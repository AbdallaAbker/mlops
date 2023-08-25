import datetime

import numpy as np
from sklearn import datasets

from evidently.metric_preset import DataDriftPreset
from evidently.metrics import DatasetCorrelationsMetric, ColumnDriftMetric, ColumnMissingValuesMetric
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns
from evidently.tests import TestShareOfDriftedColumns
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.workspace import Workspace

adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame

adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
adult_cur.iloc[200:500, 3:5] = np.nan

WORKSPACE = "workspace"


def create_report(i: int, tags=[]):
    data_drift_report = Report(
        metrics=[
            DataDriftPreset(),
            #ColumnDriftMetric(column_name="age"),
            #ColumnMissingValuesMetric(column_name="age")
            ], 
        metadata={"type": "data_quality"}, 
        tags=tags, 
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i), 
    )

    data_drift_report.set_batch_size("daily")
    data_drift_report.set_dataset_id("adult")

    data_drift_report.run(reference_data=adult_ref, current_data=adult_cur.iloc[100*i:100*(i+1), :])
    return data_drift_report


def create_test_suite():
    data_drift_dataset_tests = TestSuite(
        tests=[
            TestNumberOfDriftedColumns(),
            TestShareOfDriftedColumns(),
        ]
    )

    data_drift_dataset_tests.run(reference_data=adult_ref, current_data=adult_cur)
    return data_drift_dataset_tests


def create_project(workspace: Workspace):
    project = workspace.create_project("Example Project")
    project.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="My beautiful panels",
        )
    )
    project.add_panel(
        DashboardPanelPlot(
            title="drift_panel",
            filter=ReportFilter(metadata_values={"type": "data_quality"}, tag_values=[ ]),
            values=[
                PanelValue(metric_id="DatasetDriftMetric", field_path="share_of_drifted_columns", legend="Share"),
                PanelValue(metric_id="DatasetDriftMetric", field_path="number_of_drifted_columns", legend="Count"),
            ],
            plot_type=PlotType.LINE,
        )
    )
    project.add_panel(
        DashboardPanelPlot(
            title="age_data_drift_panel",
            filter=ReportFilter(metadata_values={"type": "data_quality"}, tag_values=[]),
            values=[
                PanelValue(metric_id="ColumnDriftMetric", field_path="drift_score", legend="drift (wasserstein)"),
            ],
            plot_type=PlotType.LINE,
            size=1
        )
    )
    project.add_panel(
        DashboardPanelPlot(
            title="age_missing_values_panel",
            filter=ReportFilter(metadata_values={"type": "data_quality"}, tag_values=[]),
            values=[
                PanelValue(metric_id="ColumnMissingValuesMetric", field_path="share_of_missing_values", legend="Share"),
                PanelValue(metric_id="ColumnMissingValuesMetric", field_path="number_of_missing_values", legend="Count"),
            ],
            plot_type=PlotType.LINE,
            size=1
        )
    )    
    return project


def main(workspace: str):
    ws = Workspace.create(workspace)
    project = create_project(ws)
    project.save()

    for i in range(0, 19):
        report = create_report(i=i)
        ws.add_report(project.id, report)

    test_suite = create_test_suite()
    ws.add_test_suite(project.id, test_suite)


if __name__ == "__main__":
    main("workspace")
