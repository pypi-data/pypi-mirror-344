from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from athina_client.services import AthinaApiService
from athina_client.constants import MAX_DATASET_ROWS

@dataclass
class Dataset:
    id: str
    source: str
    name: str
    description: Optional[str] = None
    language_model_id: Optional[str] = None
    prompt_template: Optional[Any] = None
    rows: List[Dict[str, Any]] = field(default_factory=list)
    project_name: Optional[str] = None

    @staticmethod
    def _check_forbidden_keys(rows: List[Dict[str, Any]]):
        """
        Helper method to check if any row contains the forbidden key '__id'.

        Args:
            rows (List[Dict[str, Any]]): A list of rows to check.

        Raises:
            ValueError: If any row contains the '__id' key.
        """
        for row in rows:
            if "__id" in row:
                raise ValueError("Dataset rows cannot contain the '__id' key.")

    @staticmethod
    def create(
        name: str,
        description: Optional[str] = None,
        rows: Optional[List[Dict[str, Any]]] = None,
        eval_columns: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        project_name: Optional[str] = None,
    ) -> "Dataset":
        """
        Creates a new dataset with the provided details and rows.

        Args:
            name (str): The name of the dataset.
            description (Optional[str]): A brief description of the dataset.
            language_model_id (Optional[str]): The ID of the language model used.
            prompt_template (Optional[Any]): The prompt template associated with the dataset.
            rows (List[Dict[str, Any]]): A list of rows to include in the dataset.
            eval_columns (List[str, Any]): A list of column names that should be treated as evals.
            project_name (Optional[str]): The name of the project in which this dataset belongs to.

        Returns:
            Dataset: An instance of the Dataset class representing the newly created dataset.
        """
        rows = rows or []
        eval_columns = eval_columns or []
        Dataset._check_forbidden_keys(rows)

        dataset_data = {
            "source": "dev_sdk",
            "name": name,
            "description": description,
            "dataset_rows": rows,
            "eval_columns": eval_columns,
            "metadata": metadata,
            "tags": tags,
            "project_name": project_name if project_name is not None else None,
        }

        dataset_data = {k: v for k, v in dataset_data.items() if v is not None}

        try:
            created_dataset_data = AthinaApiService.create_dataset(dataset_data)
        except Exception as e:
            raise

        dataset = Dataset(
            id=created_dataset_data["id"],
            source=created_dataset_data["source"],
            name=created_dataset_data["name"],
            description=created_dataset_data["description"],
            language_model_id=created_dataset_data["language_model_id"],
            prompt_template=created_dataset_data["prompt_template"],
            project_name=created_dataset_data.get("project_name"),
        )
        return dataset

    @staticmethod
    def change_project(dataset_id: str, project_name: str) -> Dict[str, Any]:
        """
        Changes the project of a dataset.

        Args:
            dataset_id (str): The ID of the dataset to change the project for.
            project_name (str): The name of the project.

        Returns:
            Dict[str, Any]: The response from the API after changing the project.

        Raises:
            CustomException: If the API call fails or returns an error.
        """
        try:
            response = AthinaApiService.change_dataset_project(dataset_id, project_name)
            return response
        except Exception as e:
            raise CustomException("Error changing project for dataset", str(e))

    @staticmethod
    def add_rows(dataset_id: str, rows: List[Dict[str, Any]]):
        """
        Adds rows to an existing dataset in batches.

        Args:
            - dataset_id (str): The ID of the dataset to which rows will be added.
            - rows (List[Dict[str, Any]]): A list of rows to be added to the dataset.
        Raises:
            - Exception: If the API returns an error or the limit of 5000 rows is exceeded.
        """
        Dataset._check_forbidden_keys(rows)

        batch_size = 100
        for i in range(0, len(rows), batch_size):
            batch = rows[i : i + batch_size]
            try:
                AthinaApiService.add_dataset_rows(dataset_id, batch)
            except Exception as e:
                raise

    @staticmethod
    def list_datasets() -> List["Dataset"]:
        """
        Retrieves a list of all datasets available.

        Returns:
            List[Dataset]: A list of Dataset instances representing all available datasets.
        """
        try:
            datasets = AthinaApiService.list_datasets()
        except Exception as e:
            raise
        return [
            Dataset(
                id=dataset["id"],
                source=dataset["source"],
                name=dataset["name"],
                description=dataset["description"],
                language_model_id=dataset["language_model_id"],
                prompt_template=dataset["prompt_template"],
            )
            for dataset in datasets
        ]

    @staticmethod
    def delete_dataset_by_id(dataset_id: str) -> Dict[str, Any]:
        """
        Deletes a dataset by its ID.

        Args:
            dataset_id (str): The ID of the dataset to be deleted.

        Returns:
            Dict[str, Any]: The response from the API after deletion.
        """
        try:
            response = AthinaApiService.delete_dataset_by_id(dataset_id)
            return response
        except Exception as e:
            raise

    @staticmethod
    def get_dataset_by_id(
        dataset_id: str,
        limit: Optional[int] = MAX_DATASET_ROWS,
        offset: Optional[int] = 0,
        response_format: Optional[str] = "flat",
        include_dataset_annotations: Optional[bool] = False
    ) -> Dict[str, Any]:
        """
        Retrieves a dataset by its ID and formats the response based on the provided format.

        Args:
            dataset_id (str): The ID of the dataset to retrieve.
            limit (Optional[int]): Maximum number of dataset rows to return per page. Defaults to MAX_DATASET_ROWS.
            offset (Optional[int]): Page number (zero-indexed) for pagination of dataset rows. Defaults to 0 (first page).
            response_format (Optional[str]): The format of the response, either 'flat' or 'detailed'. Defaults to 'flat'.
            include_dataset_annotations (Optional[bool]): Whether to include dataset annotations in the response. If True, annotations will be included; if False, they will be excluded. Defaults to False.

        Returns:
            Dict[str, Any]: The cleaned and formatted dataset information.
        """
        try:
            response = AthinaApiService.get_dataset_by_id(dataset_id, limit=limit, offset=offset, include_dataset_annotations=include_dataset_annotations)
            return Dataset._clean_response(response, response_format)
        except Exception as e:
            raise

    @staticmethod
    def get_dataset_by_name(
        name: str,
        limit: Optional[int] = MAX_DATASET_ROWS,
        offset: Optional[int] = 0,
        response_format: Optional[str] = "flat",
        include_dataset_annotations: Optional[bool] = False
    ) -> Dict[str, Any]:
        """
        Retrieves a dataset by its name and formats the response based on the provided format.

        Args:
            name (str): The name of the dataset to retrieve.
            limit (Optional[int]): Maximum number of dataset rows to return per page. Defaults to MAX_DATASET_ROWS.
            offset (Optional[int]): Page number (zero-indexed) for pagination of dataset rows. Defaults to 0 (first page).
            response_format (Optional[str]): The format of the response, either 'flat' or 'detailed'. Defaults to 'flat'.
            include_dataset_annotations (Optional[bool]): Whether to include dataset annotations in the response. If True, annotations will be included; if False, they will be excluded. Defaults to False.

        Returns:
            Dict[str, Any]: The cleaned and formatted dataset information.
        """
        try:
            response = AthinaApiService.get_dataset_by_name(name, limit=limit, offset=offset, include_dataset_annotations=include_dataset_annotations)
            return Dataset._clean_response(response, response_format)
        except Exception as e:
            raise

    @staticmethod
    def dataset_link(dataset_id: str) -> str:
        """
        Generates a link to the dataset on the Athina platform.

        Args:
            dataset_id (str): The ID of the dataset.

        Returns:
            str: A URL linking to the dataset on the Athina platform.
        """
        return f"https://app.athina.ai/develop/{dataset_id}"

    def _clean_response(
        response: Dict[str, Any], response_format: str
    ) -> Dict[str, Any]:
        """
        Cleans and formats the API response by removing unnecessary keys and modifying the dataset evaluation results.

        Args:
            response (Dict[str, Any]): The raw API response containing dataset information.
            response_format (str): The format of the response, either 'flat' or 'detailed'.

        Returns:
            Dict[str, Any]: The cleaned and formatted dataset information.
        """
        dataset = response.get("dataset", {})
        dataset_rows = response.get("dataset_rows", [])
        development_eval_configs = response.get("development_eval_configs", [])

        # Create a lookup for development_eval_configs by id
        eval_config_lookup = {
            config["id"]: {
                "display_name": config["display_name"],
                "eval_type_id": config["eval_type_id"],
            }
            for config in development_eval_configs
        }

        # Clean dataset rows
        for row in dataset_rows:
            for config_id, config_data in eval_config_lookup.items():
                eval_result = next(
                    (
                        er
                        for er in row.get("dataset_eval_results", [])
                        if er.get("development_eval_config_id") == config_id
                    ),
                    None,
                )

                if eval_result:
                    metric_value = eval_result.get("metric_value")

                    # Attempt to convert to an int if possible, otherwise float, otherwise keep as-is
                    try:
                        metric_value = int(metric_value)
                    except (ValueError, TypeError):
                        try:
                            metric_value = float(metric_value)
                        except (ValueError, TypeError):
                            pass  # Keep it as-is if it's not a number

                    if response_format == "detailed":
                        metric_id = eval_result.get("metric_id")
                        explanation = eval_result.get("explanation")

                        # Set "Ragas Faithfulness Test" to None if metric_id is None
                        if metric_id is None:
                            row[f"{config_data['display_name']}"] = None
                        else:
                            row[f"{config_data['display_name']}"] = {
                                "metric_id": metric_id,
                                "metric_value": metric_value,
                                "explanation": explanation,
                            }
                    elif response_format == "flat":
                        row[f"{config_data['display_name']}"] = metric_value
                else:
                    if response_format == "detailed":
                        row[f"{config_data['display_name']}"] = None
                    elif response_format == "flat":
                        row[f"{config_data['display_name']}"] = None

            # Remove the original dataset_eval_results array
            row.pop("dataset_eval_results", None)

        cleaned_response = {
            "dataset": {
                "id": dataset.get("id"),
                "source": dataset.get("source"),
                "user_id": dataset.get("user_id"),
                "org_id": dataset.get("org_id"),
                "workspace_slug": dataset.get("workspace_slug"),
                "name": dataset.get("name"),
                "description": dataset.get("description"),
                "language_model_id": dataset.get("language_model_id"),
                "prompt_template": dataset.get("prompt_template"),
                "reference_dataset_id": dataset.get("reference_dataset_id"),
                "created_at": dataset.get("created_at"),
                "updated_at": dataset.get("updated_at"),
                "reference_dataset": dataset.get("reference_dataset"),
                "derived_datasets": dataset.get("derived_datasets", []),
                "datacolumn": dataset.get("datacolumn", []),
            },
            "dataset_rows": dataset_rows,
        }

        if "dataset_annotations" in response:
            cleaned_response["dataset_annotations"] = response.get("dataset_annotations")

        if "annotated_users" in response:
            cleaned_response["annotated_users"] = response.get("annotated_users")

        return cleaned_response

    @staticmethod
    def update_cells(dataset_id: str, cells: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Updates specific cells in a dataset.

        Args:
            dataset_id (str): The ID of the dataset to update cells in.
            cells (List[Dict[str, Any]]): A list of cells to update, where each cell is a dictionary containing:
                - row_no (int): The row number of the cell to update (1-based indexing).
                - column_name (str): The name of the column containing the cell to update.
                - value (Any): The new value for the specified cell.

        Returns:
            Dict[str, Any]: The response from the API after updating the cells.

        Raises:
            CustomException: If the API call fails or returns an error.
        
        Example:
            ```python
            cells_to_update = [
                {"row_no": 1, "column_name": "query", "value": "Updated query text"},
                {"row_no": 2, "column_name": "response", "value": "New model response"}
            ]
            result = Dataset.update_cells("dataset-123", cells_to_update)
            ```
        """
        try:
            response = AthinaApiService.update_dataset_cells(dataset_id, cells)
            return response
        except Exception as e:
            raise CustomException("Error updating cells in dataset", str(e))
