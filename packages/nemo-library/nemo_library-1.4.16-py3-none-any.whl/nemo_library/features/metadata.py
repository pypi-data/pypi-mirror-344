from collections import defaultdict
import copy
from dataclasses import fields, is_dataclass
import json
import logging
from pathlib import Path
import re
from typing import Type, TypeVar
from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.nemo_persistence_api import (
    _deserializeMetaDataObject,
    createApplications,
    createAttributeGroups,
    createAttributeLinks,
    createDefinedColumns,
    createDiagrams,
    createMetrics,
    createPages,
    createReports,
    createRules,
    createSubProcesses,
    createTiles,
    deleteApplications,
    deleteAttributeGroups,
    deleteAttributeLinks,
    deleteDefinedColumns,
    deleteDiagrams,
    deleteMetrics,
    deletePages,
    deleteReports,
    deleteRules,
    deleteSubprocesses,
    deleteTiles,
    getApplications,
    getAttributeGroups,
    getAttributeLinks,
    getDefinedColumns,
    getDiagrams,
    getImportedColumns,
    getMetrics,
    getPages,
    getRules,
    getSubProcesses,
    getTiles,
)
from nemo_library.features.nemo_persistence_api import (
    getDependencyTree,
)
from nemo_library.features.nemo_persistence_api import (
    getReports,
)
from nemo_library.model.application import Application
from nemo_library.model.attribute_group import AttributeGroup
from nemo_library.model.attribute_link import AttributeLink
from nemo_library.model.defined_column import DefinedColumn
from nemo_library.model.dependency_tree import DependencyTree
from nemo_library.model.diagram import Diagram
from nemo_library.model.imported_column import ImportedColumn
from nemo_library.model.metric import Metric
from nemo_library.model.pages import Page
from nemo_library.model.report import Report
from nemo_library.model.rule import Rule
from nemo_library.model.tile import Tile
from nemo_library.model.subprocess import SubProcess
from nemo_library.utils.config import Config
from nemo_library.utils.utils import FilterType, FilterValue

__all__ = ["MetaDataLoad", "MetaDataDelete", "MetaDataCreate"]

T = TypeVar("T")


def MetaDataLoad(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    functions = {
        "applications": getApplications,
        "attributegroups": getAttributeGroups,
        "attributelinks": getAttributeLinks,
        "definedcolumns": getDefinedColumns,
        "diagrams": getDiagrams,
        "metrics": getMetrics,
        "pages": getPages,
        "reports": getReports,
        "rules": getRules,
        "tiles": getTiles,
        "subprocesses": getSubProcesses,
    }

    for name, func in functions.items():
        logging.info(f"load {name} from NEMO")
        data = func(
            config=config,
            projectname=projectname,
            filter=filter,
            filter_type=filter_type,
            filter_value=filter_value,
        )

        _export_data_to_json(config, name, data)


def MetaDataDelete(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    get_functions = {
        "applications": getApplications,
        "attributegroups": getAttributeGroups,
        "attributelinks": getAttributeLinks,
        "definedcolumns": getDefinedColumns,
        "diagrams": getDiagrams,
        "metrics": getMetrics,
        "pages": getPages,
        "reports": getReports,
        "rules": getRules,
        "subprocesses": getSubProcesses,
        "tiles": getTiles,
    }

    delete_functions = {
        "subprocesses": deleteSubprocesses,
        "applications": deleteApplications,
        "pages": deletePages,
        "tiles": deleteTiles,
        "metrics": deleteMetrics,
        "definedcolumns": deleteDefinedColumns,
        "attributelinks": deleteAttributeLinks,
        "attributegroups": deleteAttributeGroups,
        "diagrams": deleteDiagrams,
        "reports": deleteReports,
        "rules": deleteRules,
    }

    for name, func in get_functions.items():
        logging.info(f"delete {name} from NEMO")
        data = func(
            config=config,
            projectname=projectname,
            filter=filter,
            filter_type=filter_type,
            filter_value=filter_value,
        )

        objects_to_delete = [obj.id for obj in data]

        delete_functions[name](config=config, **{name: objects_to_delete})


def MetaDataCreate(
    config: Config,
    projectname: str,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
) -> None:

    # load data from model (JSON)
    logging.info(f"load model from JSON files in folder {config.get_metadata()}")
    applications_model = _load_data_from_json(config, "applications", Application)
    attributegroups_model = _load_data_from_json(
        config, "attributegroups", AttributeGroup
    )
    attributelinks_model = _load_data_from_json(config, "attributelinks", None)
    definedcolumns_model = _load_data_from_json(config, "definedcolumns", DefinedColumn)
    diagrams_model = _load_data_from_json(config, "diagrams", Diagram)
    metrics_model = _load_data_from_json(config, "metrics", Metric)
    pages_model = _load_data_from_json(config, "pages", Page)
    reports_model = _load_data_from_json(config, "reports", Report)
    rules_model = _load_data_from_json(config, "rules", Rule)
    subprocesses_model = _load_data_from_json(config, "subprocesses", SubProcess)
    tiles_model = _load_data_from_json(config, "tiles", Tile)

    # sort attribute groups
    hierarchy, _ = _attribute_groups_build_hierarchy(attributegroups_model)
    attributegroups_model = attribute_groups_sort_hierarchy(hierarchy, root_key=None)

    # load data from NEMO
    logging.info(f"load model from NEMO files from project {projectname}")
    applications_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getApplications,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributegroups_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeGroups,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributelinks_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeLinks,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    definedcolumns_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getDefinedColumns,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    diagrams_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getDiagrams,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    metrics_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getMetrics,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    pages_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getPages,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    reports_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getReports,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    tiles_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getTiles,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    rules_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getRules,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    subprocesses_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getSubProcesses,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )

    # reconcile data
    deletions: dict[str, list[T]] = {}
    updates: dict[str, list[T]] = {}
    creates: dict[str, list[T]] = {}

    logging.info(f"reconcile both models")
    for key, model_list, nemo_list in [
        ("applications", applications_model, applications_nemo),
        ("attributegroups", attributegroups_model, attributegroups_nemo),
        ("attributelinks", attributelinks_model, attributelinks_nemo),
        ("definedcolumns", definedcolumns_model, definedcolumns_nemo),
        ("diagrams", diagrams_model, diagrams_nemo),
        ("metrics", metrics_model, metrics_nemo),
        ("pages", pages_model, pages_nemo),
        ("reports", reports_model, reports_nemo),
        ("tiles", tiles_model, tiles_nemo),
        ("rules", rules_model, rules_nemo),
        ("subprocesses", subprocesses_model, subprocesses_nemo),
    ]:
        nemo_list_cleaned = copy.deepcopy(nemo_list)
        nemo_list_cleaned = _clean_fields(nemo_list_cleaned)

        deletions[key] = _find_deletions(model_list, nemo_list)
        updates[key] = _find_updates(model_list, nemo_list_cleaned)
        creates[key] = _find_new_objects(model_list, nemo_list)

    # Start with deletions
    logging.info(f"start deletions")
    delete_functions = {
        "applications": deleteApplications,
        "pages": deletePages,
        "tiles": deleteTiles,
        "metrics": deleteMetrics,
        "definedcolumns": deleteDefinedColumns,
        "attributegroups": deleteAttributeGroups,
        "attributelinks": deleteAttributeLinks,
        "diagrams": deleteDiagrams,
        "rules": deleteRules,
        "reports": deleteReports,
        "subprocesses": deleteSubprocesses,
    }

    for key, delete_function in delete_functions.items():
        if deletions[key]:
            objects_to_delete = [data_nemo.id for data_nemo in deletions[key]]
            delete_function(config=config, **{key: objects_to_delete})

    # Now do updates and creates in a reverse  order
    logging.info(f"start creates and updates")
    create_functions = {
        "attributegroups": createAttributeGroups,
        "reports": createReports,
        "rules": createRules,
        "diagrams": createDiagrams,
        "attributelinks": createAttributeLinks,
        "definedcolumns": createDefinedColumns,
        "metrics": createMetrics,
        "tiles": createTiles,
        "pages": createPages,
        "applications": createApplications,
        "subprocesses": createSubProcesses,
    }

    for key, create_function in create_functions.items():
        # create new objects first
        if creates[key]:
            create_function(
                config=config, projectname=projectname, **{key: creates[key]}
            )
        # now the changes
        if updates[key]:
            create_function(
                config=config, projectname=projectname, **{key: updates[key]}
            )

    # reconcile of order in focus not possible at the moment
    return

    # sub processes and focus order depends on dependency tree for objects
    # refresh data from server
    logging.info(f"get dependency tree for metrics")
    metrics_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getMetrics,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributegroups_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeGroups,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )
    attributelinks_nemo = _fetch_data_from_nemo(
        config=config,
        projectname=projectname,
        func=getAttributeLinks,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )

    dependency_tree = {
        metric.internalName: _collect_node_objects(d)
        for metric in metrics_nemo
        if (d := getDependencyTree(config=config, id=metric.id)) is not None
    }

    # reconcile focus order now
    logging.info(f"reconcile order in focus")
    for metric_internal_name, values in dependency_tree.items():

        # find metric in model
        metric = None
        for metric_search in metrics_model:
            if metric_search.internalName == metric_internal_name:
                metric = metric_search
                break
        if not metric:
            logging.error(f"metric {metric_internal_name} not found in model")
            continue

        # check whether we need some new links
        new_links = []
        for element in values:

            # linked attribute are support for imported columns only
            if element.nodeType == "ExportedColumn":
                # check whether we have this linked attribute already
                link_found = False
                for link in attributelinks_nemo:
                    if (
                        link.sourceAttributeId == element.nodeId
                        and link.parentAttributeGroupInternalName
                        == metric.parentAttributeGroupInternalName
                    ):
                        link_found = True
                        break
                if not link_found:
                    logging.info(
                        f"create linked attribute {metric.internalName} - {element.nodeInternalName}"
                    )
                    new_link = AttributeLink(
                        sourceAttributeId=element.nodeId,
                        parentAttributeGroupInternalName=metric.parentAttributeGroupInternalName,
                        displayName=f"{metric.internalName} - {element.nodeInternalName}",
                    )
                    new_links.append(new_link)
                    attributelinks_nemo.append(
                        new_link
                    )  # add link here, we don't want to create it twice

        # createAttributeLinks(
        #     config=config,
        #     projectname=projectname,
        #     attributeLinks=new_links,
        # )


def _date_columns(
    columns: list[str], imported_columns: list[ImportedColumn]
) -> list[str]:
    date_cols = []
    for col in columns:
        ic = None
        for ic_search in imported_columns:
            if ic_search.internalName == col:
                ic = ic_search

        if ic and ic.dataType == "date":
            date_cols.append(col)

    return date_cols


def _collect_node_objects(tree: DependencyTree) -> list[str]:
    elements = [tree]
    for dep in tree.dependencies:
        elements.extend(_collect_node_objects(dep))
    return elements


def _attribute_groups_build_hierarchy(attribute_groups):
    hierarchy = defaultdict(list)
    group_dict = {group.internalName: group for group in attribute_groups}

    for group in attribute_groups:
        parent_name = group.parentAttributeGroupInternalName
        hierarchy[parent_name].append(group)

    return hierarchy, group_dict


def attribute_groups_sort_hierarchy(hierarchy, root_key=None):
    sorted_list = []

    def add_children(parent):
        for child in sorted(hierarchy.get(parent, []), key=lambda x: x.displayName):
            sorted_list.append(child)
            add_children(child.internalName)

    add_children(root_key)
    return sorted_list


def _fetch_data_from_nemo(
    config: Config,
    projectname: str,
    func,
    filter: str = "*",
    filter_type: FilterType = FilterType.STARTSWITH,
    filter_value: FilterValue = FilterValue.DISPLAYNAME,
):
    return func(
        config=config,
        projectname=projectname,
        filter=filter,
        filter_type=filter_type,
        filter_value=filter_value,
    )


def _load_data_from_json(config, file: str, cls: Type[T]) -> list[T]:
    """
    Loads JSON data from a file and converts it into a list of DataClass instances,
    handling nested structures recursively.
    """
    path = Path(config.get_metadata()) / f"{file}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [_deserializeMetaDataObject(item, cls) for item in data]


def _find_deletions(model_list: list[T], nemo_list: list[T]) -> list[T]:
    model_keys = {obj.internalName for obj in model_list}
    return [obj for obj in nemo_list if obj.internalName not in model_keys]


def _find_updates(model_list: list[T], nemo_list: list[T]) -> list[T]:
    updates = []
    nemo_dict = {getattr(obj, "internalName"): obj for obj in nemo_list}
    for model_obj in model_list:
        key = getattr(model_obj, "internalName")
        if key in nemo_dict:
            nemo_obj = nemo_dict[key]
            if is_dataclass(model_obj) and is_dataclass(nemo_obj):
                differences = {
                    attr.name: (
                        getattr(model_obj, attr.name),
                        getattr(nemo_obj, attr.name),
                    )
                    for attr in fields(model_obj)
                    if getattr(model_obj, attr.name) != getattr(nemo_obj, attr.name)
                }

            if differences:
                for attrname, (new_value, old_value) in differences.items():
                    logging.info(f"{attrname}: {old_value} --> {new_value}")
                updates.append(model_obj)

    return updates


def _find_new_objects(model_list: list[T], nemo_list: list[T]) -> list[T]:
    nemo_keys = {getattr(obj, "internalName") for obj in nemo_list}
    return [obj for obj in model_list if getattr(obj, "internalName") not in nemo_keys]


def _export_data_to_json(config: Config, file: str, data):
    data = _clean_fields(data)
    path = Path(config.get_metadata()) / f"{file}.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            [element.to_dict() for element in data], file, indent=4, ensure_ascii=True
        )


def _clean_fields(data):
    for element in data:
        element.id = ""
        element.tenant = ""
        element.projectId = ""
        element.tileSourceID = ""
        element.focusOrder = ""

        if isinstance(element, Diagram):
            for value in element.values:
                value.id = ""

        elif isinstance(element, Page):
            for visual in element.visuals:
                visual.id = ""

    return data


def _extract_fields(formulas_dict):
    field_pattern = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")

    extracted_fields = {}

    for key, formulas in formulas_dict.items():
        extracted_fields[key] = set()
        for formula in formulas:
            if isinstance(formula, str) and formula.strip():
                fields = field_pattern.findall(formula)
                extracted_fields[key].update(fields)

    return {k: sorted(v) for k, v in extracted_fields.items()}
