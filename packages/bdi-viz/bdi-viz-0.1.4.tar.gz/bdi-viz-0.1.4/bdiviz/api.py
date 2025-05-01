import hashlib
import json
import logging
import warnings
from datetime import datetime
from os import getenv, makedirs
from os.path import dirname, exists, expanduser, join
from typing import Any, Dict, List, Optional, Tuple, Union

import altair as alt
import datamart_profiler
import numpy as np
import pandas as pd
import panel as pn
from bdikit.mapping_algorithms.column_mapping.topk_matchers import (
    CLTopkColumnMatcher,
    ColumnScore,
    TopkColumnMatcher,
    TopkMatching,
)
from bdikit.models.contrastive_learning.cl_api import DEFAULT_CL_MODEL
from bdikit.utils import get_gdc_layered_metadata, read_gdc_schema
from polyfuzz import PolyFuzz
from polyfuzz.models import RapidFuzz
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

from bdiviz.utils import LLMAssistant

GDC_DATA_PATH = join(dirname(__file__), "resource/gdc_table.csv")
default_os_cache_dir = getenv("XDG_CACHE_HOME", join(expanduser("~"), ".cache"))
BDIVIZ_CACHE_DIR = getenv("BDIVIZ_CACHE", join(default_os_cache_dir, "bdiviz"))
makedirs(BDIVIZ_CACHE_DIR, exist_ok=True)

# Schema.org types
SCHEMA_ENUMERATION = "http://schema.org/Enumeration"
SCHEMA_TEXT = "http://schema.org/Text"
SCHEMA_FLOAT = "http://schema.org/Float"
SCHEMA_INTEGER = "http://schema.org/Integer"
SCHEMA_BOOLEAN = "http://schema.org/Boolean"


logger = logging.getLogger("bdiviz")
warnings.filterwarnings("ignore")
logger_datamart = logging.getLogger("datamart_profiler")
logger_datamart.setLevel(logging.CRITICAL)

pn.extension("tabulator")  # type: ignore
pn.extension("mathjax")  # type: ignore
pn.extension("vega")  # type: ignore
pn.extension("floatpanel")  # type: ignore
pn.extension("jsoneditor")  # type: ignore


class BDISchemaMatchingHeatMap(TopkColumnMatcher):
    def __init__(
        self,
        source: pd.DataFrame,
        target: Union[pd.DataFrame, str] = "gdc",
        top_k: int = 10,
        heatmap_recommendations: Optional[List[Dict]] = None,
        max_chars_samples: int = 150,
        height: int = 600,
        ai_assitant: bool = False,
    ) -> None:
        """
        BDISchemaMatchingHeatMap is a class for generating and visualizing schema matching heatmaps between a source DataFrame and a target DataFrame or predefined dataset.

        :param source: The source DataFrame containing the columns to be matched.
        :type source: pd.DataFrame
        :param target: The target DataFrame or a string identifier for a predefined dataset (default is "gdc").
        :type target: Union[pd.DataFrame, str]
        :param top_k: The number of top matches to consider for each source column (default is 10).
        :type top_k: int
        :param heatmap_recommendations: Optional precomputed heatmap recommendations (default is None).
        :type heatmap_recommendations: Optional[List[Dict]]
        :param max_chars_samples: Maximum number of characters for sample values (default is 150).
        :type max_chars_samples: int
        :param height: Height of the heatmap visualization (default is 600).
        :type height: int
        :param ai_assitant: Flag to enable AI assistant for recommendations (default is False).
        :type ai_assitant: bool
        """
        self.json_path = "heatmap_recommendations.json"

        # Sources color palette
        self.source_prefix = ""
        self.source_colors = [
            "#ffa600",
            "#ff6361",
            "#bc5090",
            "#58508d",
            "#003f5c",
        ]

        # Source and target data
        self.source = source.sample(
            min(1000, len(source)), random_state=42
        ).reset_index(drop=True)
        self.target = target

        # Source columns lookup
        self.source_columns = [
            (column, self.source_prefix) for column in source.columns
        ]

        self.top_k = max(1, min(top_k, 40))

        self.rec_list_df: Optional[pd.DataFrame] = None
        self.rec_cols: Optional[List[str]] = None
        self.subschemas = None

        # Selected column
        self.selected_row = None

        # Embeddings
        self.l_features = self._load_cached_features("l")
        self.r_features = self._load_cached_features("r")

        # Load cached results
        cached_heatmap_recommendations = self._load_cached_results()
        if cached_heatmap_recommendations is not None:
            self.heatmap_recommendations = cached_heatmap_recommendations
        else:
            self.heatmap_recommendations = self._generate_top_k_matches()
            self._cache_results(self.heatmap_recommendations)

        self._write_json(self.heatmap_recommendations)

        self.candidates_dfs = self._clean_heatmap_recommendations()

        self.height = height

        # Undo/Redo
        # The undo/redo stack is a list of data
        # Data is like this: {'Candidate column': 'Country', 'Top k columns': [['country_of_birth', '0.5726'], ...]}
        self.undo_stack = []
        self.redo_stack = []
        self.logs = []

        self._get_heatmap()
        self.clusters = self._gen_clusters()

        # Value matches
        self.value_matches_dfs = self._generate_all_value_matches()

        # AI Assistant
        self.assistant = None
        if ai_assitant:
            self.assistant = LLMAssistant()
            self.chat_history = []

        # Panel configurations
        self.panel_floatpanel_config = {"headerControls": {"close": "remove"}}
        self.ai_assistant_status = "minimized"
        self.log_status = "minimized"

    def _generate_top_k_matches(self) -> List[Dict]:
        if isinstance(self.target, pd.DataFrame):
            target_df = self.target
        elif self.target == "gdc":
            target_df = pd.read_csv(GDC_DATA_PATH)
        else:
            raise ValueError("Invalid target value. Must be a DataFrame or 'gdc'.")

        topk_matcher = CLTopkColumnMatcher(model_name=DEFAULT_CL_MODEL)

        # Cache features
        if self.l_features is None:
            self.l_features = topk_matcher.api.get_embeddings(self.source)
            self._cache_features("l")
        if self.r_features is None:
            self.r_features = topk_matcher.api.get_embeddings(target_df)
            self._cache_features("r")

        top_k_matches = self._generate_top_k_matches_from_embeddings(
            self.source, target_df, self.l_features, self.r_features
        )

        output_json = []
        for match in top_k_matches:
            source_dict = {
                "source_column": match["source_column"],
                "top_k_columns": [],
                "source_dataset": self.source_prefix,
            }
            for column in match["top_k_columns"]:
                source_dict["top_k_columns"].append(  # type: ignore
                    [column.column_name, float(column.score)]
                )
            output_json.append(source_dict)

        return output_json

    def _generate_top_k_matches_from_embeddings(
        self,
        source: pd.DataFrame,
        target: pd.DataFrame,
        l_features: List[np.ndarray],
        r_features: List[np.ndarray],
    ) -> List[Dict[str, Any]]:
        sim = cosine_similarity(l_features, r_features)  # type: ignore

        top_k_results = []
        for index, similarities in enumerate(sim):
            top_k_indices = np.argsort(similarities)[::-1][: self.top_k]
            top_k_columns = [
                ColumnScore(column_name=target.columns[i], score=similarities[i])
                for i in top_k_indices
            ]
            top_k_results.append(
                {
                    "source_column": source.columns[index],
                    "top_k_columns": top_k_columns,
                }
            )

        return top_k_results

    def _clean_heatmap_recommendations(self):
        candidates_dfs = {}
        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            gdc_metadata = get_gdc_layered_metadata()
            for column_data in self.heatmap_recommendations:
                column_name = column_data["source_column"]
                if column_name not in candidates_dfs:
                    recommendations = []
                else:
                    recommendations = candidates_dfs[column_name].values.tolist()
                for candidate_name, candidate_similarity in column_data[
                    "top_k_columns"
                ]:
                    subschema, gdc_data = gdc_metadata[candidate_name]
                    candidate_description = gdc_data.get("description", "")
                    candidate_type = self._gdc_get_column_type(gdc_data)
                    candidate_values = ", ".join(gdc_data.get("enum", []))
                    # candidate_values = truncate_text(candidate_values, max_chars_samples)
                    recommendations.append(
                        [
                            candidate_name,
                            candidate_similarity,
                            candidate_values,
                            candidate_type,
                            candidate_description,
                            subschema,
                        ]
                    )
                candidates_dfs[column_name] = pd.DataFrame(
                    recommendations,
                    columns=[
                        "Candidate",
                        "Similarity",
                        "Values (sample)",
                        "Type",
                        "Description",
                        "Subschema",
                    ],
                )
        elif isinstance(self.target, pd.DataFrame):
            profiled_data = datamart_profiler.process_dataset(
                self.target, coverage=False, indexes=False
            )["columns"]
            for column_data in self.heatmap_recommendations:
                column_name = column_data["source_column"]
                recommendations = []
                for candidate_name, candidate_similarity in column_data[
                    "top_k_columns"
                ]:
                    # check candidate type generated by profiler
                    profiled_cand = next(
                        profiled_cand
                        for profiled_cand in profiled_data
                        if profiled_cand["name"] == candidate_name
                    )
                    if SCHEMA_ENUMERATION in profiled_cand["semantic_types"]:
                        candidate_type = "enum"
                    elif SCHEMA_BOOLEAN in profiled_cand["semantic_types"]:
                        candidate_type = "boolean"
                    elif (
                        SCHEMA_FLOAT in profiled_cand["structural_type"]
                        or SCHEMA_INTEGER in profiled_cand["structural_type"]
                    ):
                        candidate_type = "number"
                    else:
                        candidate_type = "string"

                    candidate_values = ", ".join(
                        self.target[candidate_name].astype(str).unique()
                    )
                    recommendations.append(
                        (
                            candidate_name,
                            candidate_similarity,
                            candidate_values,
                            candidate_type,
                        )
                    )

                candidates_dfs[column_name] = pd.DataFrame(
                    recommendations,
                    columns=[
                        "Candidate",
                        "Similarity",
                        "Values (sample)",
                        "Type",
                    ],
                )
        else:
            raise ValueError("Invalid target value. Must be a DataFrame or 'gdc'.")
        return candidates_dfs

    def _load_json(self) -> "List[Dict] | None":
        cache_path = join(
            BDIVIZ_CACHE_DIR,
            f"reducings_{self._get_ground_truth_checksum()}_{self._get_data_checksum()}_{self.top_k}.tmp.json",
        )
        if exists(cache_path):
            with open(cache_path) as f:
                data = json.load(f)
                return data
        return None

    def _write_json(self, data: List[Dict]) -> None:
        self.heatmap_recommendations = data

        # cache_path = join(
        #     BDIVIZ_CACHE_DIR,
        #     f"reducings_{self._get_ground_truth_checksum()}_{self._get_data_checksum()}_{self.top_k}.tmp.json",
        # )

        # with open(cache_path, "w") as f:
        #     json.dump(data, f)

    def _get_heatmap(self) -> None:
        recommendations = self.heatmap_recommendations
        rec_cols = set()
        rec_table = []
        rec_list = []

        for d in recommendations:
            col_dict = {"Column": d["source_column"]}
            for c in d["top_k_columns"]:
                rec_cols.add(c[0])
                col_dict[c[0]] = c[1]
                rec_row = {
                    "Column": d["source_column"],
                    "Recommendation": c[0],
                    "Value": c[1],
                    "DataFrame": d["source_dataset"],
                }
                # [GDC] get description and values
                if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
                    candidates_info = self.candidates_dfs[d["source_column"]]
                    candidate_info = candidates_info[
                        candidates_info["Candidate"] == c[0]
                    ]
                    rec_row["Description"] = candidate_info["Description"].values[0]
                    rec_row["Values (sample)"] = candidate_info[
                        "Values (sample)"
                    ].values[0]
                    rec_row["Subschema"] = candidate_info["Subschema"].values[0]
                rec_list.append(rec_row)
            rec_table.append(col_dict)

        rec_cols = list(rec_cols)
        rec_cols.sort()

        rec_list_df = pd.DataFrame(rec_list)
        rec_list_df["Value"] = pd.to_numeric(rec_list_df["Value"])
        rec_list_df["DataFrame"] = rec_list_df["DataFrame"].astype(str)

        self.rec_list_df = rec_list_df
        self.rec_cols = rec_cols

        # [GDC] get subschema information
        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            self.get_cols_subschema()

    def _gen_clusters(self) -> Dict[str, List[Tuple[str, str]]]:
        knn = NearestNeighbors(
            n_neighbors=min(10, len(self.source.columns)), metric="cosine"
        )
        l_features_flat = self.l_features
        knn.fit(np.array(l_features_flat))
        clusters_idx = [
            knn.kneighbors([l_feature], return_distance=False)[0]  # type: ignore
            for l_feature in self.l_features
        ]

        clusters = {}
        for i, source_column in enumerate(self.source.columns):
            cluster_idx = clusters_idx[i]
            cluster = []
            for idx in cluster_idx:
                cluster.append(self.source_columns[idx])
            clusters[source_column] = cluster
        return clusters

    def get_cols_subschema(self) -> None:
        subschemas = []
        schema = read_gdc_schema()
        for parent, values in schema.items():
            for candidate in values["properties"].keys():
                if candidate in self.rec_cols:
                    if parent not in subschemas:
                        subschemas.append(parent)

        self.subschemas = subschemas

    def _gdc_get_column_type(self, properties: Dict) -> "str | None":
        if "enum" in properties:
            return "enum"
        elif "type" in properties:
            return properties["type"]
        else:
            return None

    def _gdc_get_column_description(self, properties: Dict) -> str:
        if "description" in properties:
            return properties["description"]
        elif "common" in properties:
            return properties["common"]["description"]
        return ""

    def _gdc_get_column_values(self, properties: Dict) -> "List[str] | None":
        col_type = self._gdc_get_column_type(properties)
        if col_type == "enum":
            return properties["enum"]
        elif col_type == "number" or col_type == "integer" or col_type == "float":
            return [
                str(properties["minimum"]) if "minimum" in properties else "-inf",
                str(properties["maximum"]) if "maximum" in properties else "inf",
            ]
        elif col_type == "boolean":
            return ["True", "False"]
        else:
            return None

    def _generate_all_value_matches(self):
        value_matches_dfs = {}
        rapidfuzz_matcher = RapidFuzz(n_jobs=1)
        value_matcher = PolyFuzz(rapidfuzz_matcher)

        for source_column, source_df in self.source_columns:
            if source_df == self.source_prefix:
                if pd.api.types.is_numeric_dtype(self.source[source_column]):
                    continue

                source_values = list(
                    self.source[source_column].dropna().unique().astype(str)
                )[:20]
            else:
                continue

            value_comparison = {
                "Source Value": source_values,
            }

            for _, row in self.candidates_dfs[source_column].iterrows():
                target_values = row["Values (sample)"].split(", ")
                value_matcher.match(source_values, target_values)
                match_results = value_matcher.get_matches()

                value_comparison[row["Candidate"]] = list(match_results["To"])

            value_matches_dfs[source_column] = pd.DataFrame(
                dict([(k, pd.Series(v)) for k, v in value_comparison.items()])
            ).fillna("")

        return value_matches_dfs

    def _accept_match(self) -> None:
        if self.selected_row is None:
            return
        col_name = self.selected_row["Column"].values[0]
        match_name = self.selected_row["Recommendation"].values[0]
        col_source_df = self.selected_row["DataFrame"].values[0]
        recommendations = self.heatmap_recommendations
        for idx, d in enumerate(recommendations):
            candidate_name = d["source_column"]
            if candidate_name != col_name:
                continue
            for top_k_name, top_k_score in d["top_k_columns"]:
                if top_k_name == match_name and col_source_df == d["source_dataset"]:
                    recommendations[idx] = {
                        "source_column": candidate_name,
                        "top_k_columns": [[top_k_name, top_k_score]],
                        "source_dataset": col_source_df,
                    }

                    # record the action
                    self._record_user_action("accept", d)
                    self._record_log("accept", candidate_name, top_k_name)

                    self._write_json(recommendations)
                    return

    def _reject_match(self) -> None:
        if self.selected_row is None:
            return
        col_name = self.selected_row["Column"].values[0]
        match_name = self.selected_row["Recommendation"].values[0]
        col_source_df = self.selected_row["DataFrame"].values[0]
        recommendations = self.heatmap_recommendations
        for idx, d in enumerate(recommendations):
            candidate_name = d["source_column"]
            if candidate_name != col_name:
                continue
            new_top_k = []
            for top_k_name, top_k_score in d["top_k_columns"]:
                if top_k_name != match_name or col_source_df != d["source_dataset"]:
                    new_top_k.append([top_k_name, top_k_score])
            recommendations[idx] = {
                "source_column": candidate_name,
                "top_k_columns": new_top_k,
                "source_dataset": col_source_df,
            }

            # record the action
            self._record_user_action("reject", d)
            self._record_log("reject", candidate_name, match_name)

            self._write_json(recommendations)
            self._get_heatmap()
            return

    def _discard_column(self, select_column: Optional[str]) -> None:
        if not select_column and select_column not in self.source.columns:
            logger.critical(f"Invalid column: {select_column}")
            return

        selected = select_column
        if self.selected_row is not None:
            selected = self.selected_row["Column"].values[0]
        logger.critical(f"Discarding column: {select_column}")
        recommendations = self.heatmap_recommendations
        for idx, d in enumerate(recommendations):
            candidate_name = d["source_column"]
            if candidate_name == selected:
                recommendations.pop(idx)
                self._write_json(recommendations)
                self._record_user_action("discard", d)
                self._record_log("discard", candidate_name, "")
                return

    def _plot_heatmap_base(self, heatmap_rec_list: pd.DataFrame) -> pn.pane.Vega:
        single = alt.selection_point(name="single")

        tooltip = [
            alt.Tooltip("Recommendation", title="Matching Candidate"),
            alt.Tooltip("Column", title="Source Column"),
            alt.Tooltip("Value", title="Similarity Score", format=".4f"),
        ]
        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            tooltip.append(alt.Tooltip("Description", title="Description"))
            tooltip.append(alt.Tooltip("Values (sample)", title="Values (sample)"))
            tooltip.append(alt.Tooltip("Subschema", title="Subschema"))
        # facet = alt.Facet(alt.Undefined)

        source_transformation = alt.datum["Column"]

        size_expr = alt.expr(f"datam.value == {single.name} ? 20 : 10")
        weight_expr = alt.expr(f"datam.value == {single.name} ? 800 : 300")

        search_input = alt.param(
            value="",
            bind=alt.binding(
                input="search",
                placeholder="Candidate search",
                name="Search ",
            ),
        )

        base = (
            alt.Chart(heatmap_rec_list)
            .transform_calculate(Column=source_transformation)
            .encode(
                y=alt.Y("Column:O", sort=None).axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    title="Source Columns",
                ),
                x=alt.X(
                    "Recommendation:O",
                    sort=None,
                ).axis(
                    labelAngle=-45,
                    labelFontSize=12,
                    titleFontSize=14,
                    title="Target Schemas",
                ),
                color=alt.condition(
                    single,
                    alt.Color("Value:Q").scale(domainMax=1, domainMin=0),
                    alt.value("lightgray"),
                ),  # type: ignore
                opacity=alt.condition(
                    alt.expr.test(
                        alt.expr.regexp(search_input, "i"), alt.datum.Recommendation
                    ),
                    alt.value(1),
                    alt.value(0.2),
                ),  # type: ignore
                tooltip=tooltip,
            )
            .add_params(single, search_input)
        )
        background = base.mark_rect()

        box_sources = []
        return pn.pane.Vega(background)

    def _update_column_selection(
        self, heatmap_rec_list: pd.DataFrame, selection: List[int]
    ) -> Tuple[str, str, str]:
        selected_idx = [selection[0] - 1]
        selected_row = heatmap_rec_list.iloc[selected_idx]
        self.selected_row = selected_row
        column = selected_row["Column"].values[0]
        rec = selected_row["Recommendation"].values[0]
        source_df = selected_row["DataFrame"].values[0]
        return column, rec, source_df

    def _gdc_candidates_info(
        self, heatmap_rec_list: pd.DataFrame, selection: List[int], n_samples: int = 20
    ) -> pn.pane.Markdown:
        if not selection:
            return pn.pane.Markdown(
                """
                
                ### Selected Recommendation
                
                *No selection.*

            """
            )
        column, rec, _ = self._update_column_selection(heatmap_rec_list, selection)
        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            df = self.candidates_dfs[column][
                self.candidates_dfs[column]["Candidate"] == rec
            ]

            rec_rank = df.index[0]
            values = df["Values (sample)"].values[0].split(", ")

            sample = "\n\n"
            for _, v in enumerate(values[:n_samples]):
                sample += f"""            - {v}\n"""
            if len(values) == 0:
                sample = "*No values provided.*"
            is_sample = f" ({n_samples} samples)" if len(values) > n_samples else ""

            descrip = df.loc[rec_rank, "Description"]
            if len(df.loc[rec_rank, "Description"]) == 0:
                descrip = "*No description provided.*"

            rec_info = f"""
            ### Selected Recommendation

            **Name:** {rec}

            **Type:** {df.loc[rec_rank,'Type']}

            **Similarity:** {df.loc[rec_rank,'Similarity']}

            **Subschema:** {df.loc[rec_rank,'Subschema']}

            **Description:** {descrip}

            **Values{is_sample}:** {sample}

        """
            rec_pane = pn.pane.Markdown(rec_info)
            return rec_pane
        else:
            return pn.pane.Markdown(
                "GDC candidates info is not available for this target."
            )

    def _candidates_table(
        self, heatmap_rec_list: pd.DataFrame, selection: List[int]
    ) -> "pn.widgets.Tabulator | pn.pane.Markdown":
        if not selection:
            return pn.pane.Markdown("## No selection")
        column, rec, _ = self._update_column_selection(heatmap_rec_list, selection)
        df = self.candidates_dfs[column][
            self.candidates_dfs[column]["Candidate"] == rec
        ]

        bokeh_formatters = {
            #'Similarity': {'type': 'progress', 'min': 0.0, 'max': 1.0, 'legend': True}, # Show similarity as bars - Not working properly
            "Description": {"type": "textarea"},
            "Values (sample)": {"type": "textarea"},
        }
        text_align = {"Similarity": "center", "index": "center"}
        widths = {
            "index": "7%",
            "Candidate": "20%",
            "Similarity": "10%",
            "Description": "33%",
            "Values (sample)": "30%",
        }

        table_candidates = pn.widgets.Tabulator(
            df,
            formatters=bokeh_formatters,
            text_align=text_align,
            widths=widths,
            sizing_mode="stretch_width",
            embed_content=True,
            header_align="center",
            disabled=True,
            theme="bootstrap5",
            theme_classes=["thead-dark", "table-sm"],
        )
        return table_candidates

    def _plot_column_histogram(
        self, column: str, dataset: pd.DataFrame
    ) -> "pn.pane.Markdown | alt.LayerChart":
        if pd.api.types.is_numeric_dtype(dataset[column]):
            x = alt.Y(column, bin=True).axis(labelAngle=-45)
            text_color = "transparent"
        else:
            values = list(dataset[column].unique())
            if len(values) == len(dataset[column]) or len(values) >= 30:
                string = f"""Values are unique. 
                Some samples: {values[:5]}"""
                return pn.pane.Markdown(string)
            else:
                if np.nan in values:
                    values.remove(np.nan)
                values.sort()
                x = alt.Y(
                    column + ":N",
                    sort=values,
                ).axis(
                    None
                )  # .axis(labelAngle=-45)
            text_color = "black"

        chart = (
            alt.Chart(dataset.fillna("Null"), height=300)
            .mark_bar()
            .encode(
                x="count()",
                y=x,
            )
        )
        text = (
            alt.Chart(dataset.fillna("Null"), height=300)
            .mark_text(color=text_color, fontWeight="bold", fontSize=12, align="left")
            .encode(x="count()", y=x, text=alt.Text(column))
        )
        layered = (
            alt.layer(chart, text)
            .properties(width="container", title="Histogram of " + column)
            .configure(background="#f5f5f5")
        )
        return layered

    def _plot_source_histogram(
        self, source_column: str, heatmap_rec_list: pd.DataFrame, selection: List[int]
    ) -> "pn.pane.Markdown | alt.LayerChart":
        if not selection:
            return self._plot_column_histogram(source_column, self.source)

        column, _, source_df = self._update_column_selection(
            heatmap_rec_list, selection
        )

        if source_df == self.source_prefix:
            return self._plot_column_histogram(column, self.source)
        else:
            return pn.pane.Markdown("No source data found.")

    def _plot_target_histogram(
        self, heatmap_rec_list: pd.DataFrame, selection: List[int]
    ) -> "pn.pane.Markdown | alt.LayerChart":
        if not isinstance(self.target, pd.DataFrame):
            return pn.pane.Markdown("No ground truth provided.")
        if not selection:
            return pn.pane.Markdown("## No selection")

        _, rec, _ = self._update_column_selection(heatmap_rec_list, selection)

        return self._plot_column_histogram(rec, self.target)

    def _plot_value_comparisons(
        self, source_column: str, heatmap_rec_list: pd.DataFrame, selection: List[int]
    ) -> "pn.Column | pn.pane.Markdown":
        if not selection:
            column = source_column
            rec = None
        else:
            column, rec, _ = self._update_column_selection(heatmap_rec_list, selection)

        if column not in self.value_matches_dfs:
            return pn.pane.Markdown("No value matches found.")

        value_comparisons = self.value_matches_dfs[column]

        value_comparisons = value_comparisons[
            ["Source Value"]
            + list(
                heatmap_rec_list[heatmap_rec_list["Column"] == column]["Recommendation"]
            )
        ]

        frozen_columns = ["Source Value"]
        if rec:
            frozen_columns.append(rec)

        tabulator = pn.widgets.Tabulator(
            pd.DataFrame(
                dict([(k, pd.Series(v)) for k, v in value_comparisons.items()])
            ).fillna(""),
            frozen_columns=frozen_columns,
            show_index=False,
            width=1180,
            height=200,
        )

        value_filter = pn.widgets.TextInput(name="Value filter", value="")

        def _filter_values(df: pd.DataFrame, pattern: str):
            if not pattern or pattern == "":
                return df
            col_list = list(df.columns[:1])
            for col in df.columns[1:]:
                for value in df[col].values:
                    if pattern.lower() in str(value).lower():
                        col_list.append(col)
                    continue
            print(col_list)
            return df[col_list]

        tabulator.add_filter(pn.bind(_filter_values, pattern=value_filter))
        return pn.Column(value_filter, tabulator)

    def _plot_pane(
        self,
        select_column: Optional[str] = None,
        select_candidate_type: str = "All",
        subschemas: List[str] = [],
        n_similar: int = 0,
        threshold: float = 0.5,
        acc_click: int = 0,
        rej_click: int = 0,
        discard_click: int = 0,
        undo_click: int = 0,
        redo_click: int = 0,
        log_click: int = 0,
    ) -> pn.Column:
        if self.rec_list_df is None:
            raise ValueError("Heatmap rec_list_df not generated.")
        heatmap_rec_list = self.rec_list_df[self.rec_list_df["Value"] >= threshold]
        if select_column:
            clustered_tuples = []
            clustered_cols = []
            for cluster_key, cluster_tuples in self.clusters.items():
                if cluster_key == select_column:
                    clustered_tuples = cluster_tuples[: n_similar + 1]
                    clustered_cols = [col for col, _ in clustered_tuples]

            heatmap_rec_list = heatmap_rec_list[
                heatmap_rec_list["Column"].isin(clustered_cols)
            ]

            sort_order = {
                k: v for k, v in zip(clustered_cols, range(len(clustered_cols)))
            }
            sorted_indices = (heatmap_rec_list["Column"].map(lambda x: sort_order[x]) + (1 - heatmap_rec_list["Value"])).sort_values().index  # type: ignore
            heatmap_rec_list = heatmap_rec_list.loc[sorted_indices, :]

        candidates_df = self.candidates_dfs[select_column]

        def _filter_datatype(heatmap_rec: pd.Series) -> bool:
            if (
                candidates_df[
                    candidates_df["Candidate"] == heatmap_rec["Recommendation"]
                ]["Type"]
                == select_candidate_type
            ).any():
                return True
            else:
                return False

        if select_candidate_type != "All":
            heatmap_rec_list = heatmap_rec_list[
                heatmap_rec_list.apply(_filter_datatype, axis=1)
            ]

        if subschemas:
            subschema_rec_cols = candidates_df[
                candidates_df["Subschema"].isin(subschemas)
            ]["Candidate"].to_list()
            heatmap_rec_list = heatmap_rec_list[
                heatmap_rec_list["Recommendation"].isin(subschema_rec_cols)
            ]

        heatmap_pane = self._plot_heatmap_base(heatmap_rec_list)

        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            cand_info = pn.bind(
                self._gdc_candidates_info,
                heatmap_rec_list,
                heatmap_pane.selection.param.single,  # type: ignore
            )
        else:
            cand_info = pn.bind(
                self._plot_target_histogram,
                heatmap_rec_list,
                heatmap_pane.selection.param.single,  # type: ignore
            )

        column_hist = pn.bind(
            self._plot_source_histogram,
            select_column,
            heatmap_rec_list,
            heatmap_pane.selection.param.single,  # type: ignore
        )

        plot_history = self._plot_history()

        value_comparisons = pn.bind(
            self._plot_value_comparisons,
            select_column,
            heatmap_rec_list,
            heatmap_pane.selection.param.single,  # type: ignore
        )

        return pn.Column(
            pn.FloatPanel(
                plot_history,
                name="Operation Logs",
                width=500,
                align="end",
                theme="secondary",
                config=self.panel_floatpanel_config,
                status=self.log_status,
            ),
            pn.Row(
                heatmap_pane,
                scroll=True,
                width=1200,
                styles=dict(background="WhiteSmoke"),
            ),
            pn.Spacer(height=5),
            pn.Card(
                value_comparisons,
                title="Value Comparisons",
                styles=dict(background="WhiteSmoke"),
            ),
            pn.Card(
                pn.Row(
                    pn.Column(column_hist, width=600, scroll=True),
                    pn.Column(cand_info, width=600, scroll=True),
                ),
                title="Detailed Analysis",
                styles={"background": "WhiteSmoke"},
            ),
        )

    def _record_user_action(self, action: str, data: Dict) -> None:
        if self.redo_stack:
            self.redo_stack = []
        self.undo_stack.append((action, data))

    def _undo_user_action(self) -> None:
        if len(self.undo_stack) == 0:
            return
        action, data = self.undo_stack.pop()
        recommendations = self.heatmap_recommendations

        if action == "discard":
            recommendations.append(data)
            self.redo_stack.append((action, data))
        else:
            for idx, d in enumerate(recommendations):
                candidate_name = d["source_column"]
                if candidate_name == data["source_column"]:
                    recommendations[idx] = data
                    self.redo_stack.append((action, d))
                    break
        self._write_json(recommendations)
        self._record_log("undo", data["source_column"], "")
        self._get_heatmap()
        return

    def _redo_user_action(self) -> None:
        if len(self.redo_stack) == 0:
            return
        action, data = self.redo_stack.pop()
        recommendations = self.heatmap_recommendations

        for idx, d in enumerate(recommendations):
            if d["source_column"] == data["source_column"]:
                if action == "discard":
                    recommendations.pop(idx)
                else:
                    recommendations[idx] = data
                self.undo_stack.append((action, d))
                break
        self._write_json(recommendations)
        self._record_log("redo", data["source_column"], "")
        self._get_heatmap()
        return

    def _record_log(self, action: str, source_column: str, target_column: str) -> None:
        timestamp = datetime.now()
        self.logs.append((timestamp, action, source_column, target_column))

    def _plot_history(self) -> pn.widgets.Tabulator:
        history_dict = {
            "Timestamp": [],
            "Action": [],
            "Source Column": [],
            "Target Column": [],
        }
        for timestamp, action, source_column, target_column in self.logs:
            history_dict["Timestamp"].append(timestamp)
            history_dict["Action"].append(action)
            if action in ["accept", "reject"]:
                history_dict["Source Column"].append(source_column)
                history_dict["Target Column"].append(target_column)

            elif action in ["undo", "redo", "discard"]:
                history_dict["Source Column"].append(source_column)
                history_dict["Target Column"].append("")

        history_df = pd.DataFrame(history_dict)

        return pn.widgets.Tabulator(history_df, show_index=False)

    def _plot_chat_pane(self) -> pn.chat.ChatInterface:
        def callback(contents: str, user: Any, instance: Any) -> Optional[str]:
            if self.assistant is None:
                raise ValueError(
                    "AI Assistant not initialized, initialize it by setting ai_assitant to True."
                )
            message = self.assistant.ask(contents)
            self.chat_history.append(message)
            return message

        return pn.chat.ChatInterface(callback=callback, scroll=True)

    def plot_heatmap(self) -> pn.Column:
        """
        Plot the heatmap for the user to interact with.
        """
        select_column = pn.widgets.Select(
            name="Source Column",
            options=list(self.source.columns),
            width=120,
        )

        select_candidate_type = pn.widgets.Select(
            name="Candidate Type",
            options=["All", "enum", "number", "string", "boolean"],
            width=120,
        )

        n_similar_slider = pn.widgets.IntSlider(
            name="Similar Sources", start=0, end=5, value=0, width=150
        )
        thresh_slider = pn.widgets.FloatSlider(
            name="Candidate Threshold",
            start=0,
            end=1.0,
            step=0.01,
            value=0.1,
            width=150,
        )

        acc_button = pn.widgets.Button(name="Accept Match", button_type="success")

        rej_button = pn.widgets.Button(name="Reject Match", button_type="danger")

        discard_button = pn.widgets.Button(name="Discard Column", button_type="warning")

        undo_button = pn.widgets.Button(
            name="Undo", button_style="outline", button_type="warning"
        )
        redo_button = pn.widgets.Button(
            name="Redo", button_style="outline", button_type="primary"
        )

        ai_assistant_button = pn.widgets.Button(
            name="Show/Hide AI Assistant", button_type="primary"
        )

        log_button = pn.widgets.Button(
            name="Show/Hide Operation Log", button_type="primary"
        )

        # Subschemas
        if not isinstance(self.target, pd.DataFrame) and self.target == "gdc":
            select_rec_groups = pn.widgets.MultiChoice(
                name="Recommendation subschema", options=self.subschemas, width=180
            )
            subschema_col = pn.Column(
                select_rec_groups,
            )

        def on_click_accept_match(event: Any) -> None:
            self._accept_match()
            if (
                select_column.value
                and self.selected_row is not None
                and n_similar_slider.value == 0
            ):
                value_idx = select_column.options.index(select_column.value)
                if value_idx < len(select_column.options) - 1:
                    select_column.value = select_column.options[value_idx + 1]
            self.selected_row = None
            self._get_heatmap()

        def on_click_reject_match(event: Any) -> None:
            self._reject_match()
            self.selected_row = None

        def on_click_discard_column(event: Any) -> None:
            self._discard_column(select_column.value)
            if select_column.value and n_similar_slider.value == 0:
                value_idx = select_column.options.index(select_column.value)
                if value_idx < len(select_column.options) - 1:
                    select_column.value = select_column.options[value_idx + 1]
            self.selected_row = None
            self._get_heatmap()

        def on_click_undo(event: Any) -> None:
            self._undo_user_action()

        def on_click_redo(event: Any) -> None:
            self._redo_user_action()

        def on_click_ai_assistant(event: Any) -> None:
            if self.ai_assistant_status == "minimized":
                self.ai_assistant_status = "normalized"
            else:
                self.ai_assistant_status = "minimized"

        def on_click_log(event: Any) -> None:
            if self.log_status == "minimized":
                self.log_status = "normalized"
            else:
                self.log_status = "minimized"

        acc_button.on_click(on_click_accept_match)
        rej_button.on_click(on_click_reject_match)
        discard_button.on_click(on_click_discard_column)
        undo_button.on_click(on_click_undo)
        redo_button.on_click(on_click_redo)
        ai_assistant_button.on_click(on_click_ai_assistant)
        log_button.on_click(on_click_log)

        heatmap_bind = pn.bind(
            self._plot_pane,
            select_column,
            select_candidate_type,
            (
                select_rec_groups  # type: ignore
                if (not isinstance(self.target, pd.DataFrame) and self.target == "gdc")
                else None
            ),
            n_similar_slider,
            thresh_slider,
            acc_button.param.clicks,
            rej_button.param.clicks,
            discard_button.param.clicks,
            undo_button.param.clicks,
            redo_button.param.clicks,
            log_button.param.clicks,
        )

        buttons_down = pn.Column(acc_button, rej_button, discard_button)
        buttons_redo_undo = pn.Column(undo_button, redo_button)
        buttons_floatpanel = pn.Column(ai_assistant_button, log_button)

        column_top = pn.Row(
            select_column,
            select_candidate_type,
            # (
            #     subschema_col  # type: ignore
            #     if (not isinstance(self.target, pd.DataFrame) and self.target == "gdc")
            #     else None
            # ),
            n_similar_slider,
            thresh_slider,
            buttons_down,
            buttons_redo_undo,
            buttons_floatpanel,
            width=1200,
            styles=dict(background="WhiteSmoke"),
        )

        # AI Assistant

        if self.assistant:
            chat_pane = self._plot_chat_pane()

        def plot_ai_assistant(clicks: int) -> Optional[pn.FloatPanel]:
            if self.assistant:
                return pn.FloatPanel(
                    chat_pane,  # type: ignore
                    name="Chat with AI Assistant",
                    width=600,
                    align="end",
                    status=self.ai_assistant_status,
                    config=self.panel_floatpanel_config,
                )
            return None

        def plot_json_file(clicks: int) -> pn.Row:
            return pn.Row(
                pn.FloatPanel(
                    pn.widgets.JSONEditor(
                        value=self.heatmap_recommendations, width=500
                    ),
                    name="JSON Viewer",
                    width=540,
                    align="end",
                )
            )

        return pn.Column(
            column_top,
            pn.bind(plot_ai_assistant, ai_assistant_button.param.clicks),
            # pn.bind(plot_json_file, acc_button.param.clicks),
            pn.Spacer(height=5),
            pn.Column(heatmap_bind),
            scroll=True,
        )

    # For caching purposes
    def _get_data_checksum(self) -> str:
        return hashlib.sha1(pd.util.hash_pandas_object(self.source, index=False).values).hexdigest()  # type: ignore

    def _get_ground_truth_checksum(self) -> str:
        if isinstance(self.target, pd.DataFrame):
            gt_checksum = hashlib.sha1(
                pd.util.hash_pandas_object(self.target, index=False).values  # type: ignore
            ).hexdigest()
        else:
            gt_checksum = self.target
        return gt_checksum

    def _cache_results(self, reducings: List[Dict]) -> None:
        cache_path = join(
            BDIVIZ_CACHE_DIR,
            f"reducings_{self._get_ground_truth_checksum()}_{self._get_data_checksum()}_{self.top_k}.json",
        )
        if not exists(cache_path):
            with open(cache_path, "w") as f:
                json.dump(reducings, f)

    def _cache_features(self, feature_type: str) -> None:
        if feature_type == "l":
            features = self.l_features
            checksum = self._get_data_checksum()
        elif feature_type == "r":
            features = self.r_features
            checksum = self._get_ground_truth_checksum()
        else:
            raise ValueError("Invalid feature type.")
        features_cache_path = join(
            BDIVIZ_CACHE_DIR,
            f"features_{checksum}.ft",
        )
        if not exists(features_cache_path):
            with open(features_cache_path, "w") as f:
                for vec in features:
                    f.write(",".join([str(val) for val in vec]) + "\n")

    def _load_cached_features(self, feature_type: str) -> Optional[Dict]:
        if feature_type == "l":
            features_cache_path = join(
                BDIVIZ_CACHE_DIR,
                f"features_{self._get_data_checksum()}.ft",
            )
        elif feature_type == "r":
            features_cache_path = join(
                BDIVIZ_CACHE_DIR,
                f"features_{self._get_ground_truth_checksum()}.ft",
            )
        if exists(features_cache_path):
            with open(features_cache_path) as f:
                features = [
                    [float(val) for val in vec.split(",")]
                    for vec in f.read().split("\n")
                    if vec.strip()
                ]
                return features
        return None

    def _load_cached_results(self) -> Optional[List[Dict]]:
        cache_path = join(
            BDIVIZ_CACHE_DIR,
            f"reducings_{self._get_ground_truth_checksum()}_{self._get_data_checksum()}_{self.top_k}.json",
        )
        if exists(cache_path):
            with open(cache_path) as f:
                return json.load(f)
        return None

    def get_recommendations(
        self, source: pd.DataFrame, target: pd.DataFrame, top_k: int
    ) -> List[TopkMatching]:
        """
        Get the edited recommendations based on the user interactions.

        :param source: The source DataFrame.
        :type source: pd.DataFrame
        :param target: The target DataFrame.
        :type target: pd.DataFrame
        :param top_k: The number of top-k recommendations to return.
        :type top_k: int

        :return: The top-k recommendations.
        :rtype: List[TopkMatching]
        """
        recommendations = []
        for source_column in source.columns:
            top_k_columns = []
            for reducings in self.heatmap_recommendations:
                if reducings["source_column"] == source_column:
                    top_k_columns = [
                        ColumnScore(column_name=column[0], score=column[1])
                        for column in reducings["top_k_columns"]
                    ]
                    break
            recommendations.append(
                TopkMatching(source_column=source_column, top_k_columns=top_k_columns)
            )
        return recommendations
