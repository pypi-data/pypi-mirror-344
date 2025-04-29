"""Functions for creating a Dash app to visualize IMU data."""

import dash
import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from definitions import (
    BUFFER_SIZE,
    TUM_BLUE,
    TUM_GREY_BG,
    TUM_LIGHT_BLUE,
    UPDATE_RATE_MILLISEC,
)
from scipy.spatial.transform import Rotation
from uart_ble import LiveData, SensorData, start_imu_thread

app = dash.Dash(__name__)
app.title = "IMU Dashboard"
live_data = LiveData(buffer_size=BUFFER_SIZE)


class DashboardApp:
    """Dashboard for visualizing IMU data and orientation."""

    def __init__(self, app: Dash, live_data: LiveData) -> None:
        """Initialize the dashboard app.

        :param app: Dash app instance
        :param live_data: Dictionary containing live sensor data
        """
        self.app = app
        self.live_data = live_data
        self._register_callbacks()

    def _register_callbacks(self) -> None:
        """Register Dash callbacks for updating plots."""

        @self.app.callback(
            [
                Output("accel-plot", "figure"),
                Output("gyro-plot", "figure"),
                Output("orientation-plot", "figure"),
            ],
            Input("update-interval", "n_intervals"),
        )
        def update_dashboard(n_intervals: int):
            """Update all dashboard plots based on latest data."""
            accel_fig = self.create_time_series_figure(
                self.live_data.accel, "Accel", [TUM_BLUE, "#00BFFF", "#00FFAA"]
            )
            gyro_fig = self.create_time_series_figure(
                self.live_data.gyro, "Gyro", [TUM_LIGHT_BLUE, "#FFD700", "#FF69B4"]
            )
            orient_fig = self.create_orientation_figure(self.live_data.quat)
            return accel_fig, gyro_fig, orient_fig

    @staticmethod
    def create_orientation_figure(q: list[float]) -> go.Figure:
        """Create a 3D plot of the orientation from a quaternion.

        :param q: Quaternion as [w, x, y, z]
        :return: A 3D Plotly figure showing orientation axes
        """
        r = Rotation.from_quat(q, scalar_first=True)
        rot_matrix = r.as_matrix()

        origin = np.array([[0, 0, 0]] * 3)
        axes = rot_matrix * 0.5
        colors = [TUM_BLUE, TUM_LIGHT_BLUE, "#A2AD00"]
        labels = ["x", "y", "z"]

        origin2 = np.array([[1, 1, 1]] * 3)
        axes2 = rot_matrix * 0.5 + np.array([1, 1, 1])

        fig = go.Figure()

        for i in range(3):
            fig.add_trace(
                go.Scatter3d(
                    x=[origin[i, 0] + 0.1, axes[i, 0] + 0.1],
                    y=[origin[i, 1], axes[i, 1]],
                    z=[origin[i, 2], axes[i, 2]],
                    mode="lines+text",
                    line=dict(color=colors[i], width=6),
                    text=[None, labels[i]],
                    textposition="top center",
                    showlegend=False,
                )
            )

        for i in range(3):
            fig.add_trace(
                go.Scatter3d(
                    x=[origin2[i, 0] - 0.1, axes2[i, 0] - 0.1],
                    y=[origin2[i, 1], axes2[i, 1]],
                    z=[origin2[i, 2], axes2[i, 2]],
                    mode="lines+text",
                    line=dict(color=colors[i], width=6, dash="dot"),
                    text=[None, labels[i] + "_2"],
                    textposition="top center",
                    showlegend=False,
                )
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=TUM_GREY_BG,
            scene=dict(
                xaxis=dict(range=[-1, 2], title="X"),
                yaxis=dict(range=[-1, 2], title="Y"),
                zaxis=dict(range=[-1, 2], title="Z"),
                aspectmode="cube",
                bgcolor=TUM_GREY_BG,
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            autosize=True,
        )
        return fig

    @staticmethod
    def create_time_series_figure(
        data: SensorData, label: str, colors: list[str]
    ) -> go.Figure:
        """Create a multi-line time series plot for 3-axis IMU data.

        :param data: Dict with 'x', 'y', 'z' axis deques
        :param label: Base label for the plot title ("Accel" or "Gyro")
        :param colors: List of three hex color strings
        :return: Plotly time series figure
        """
        x_vals = np.linspace(0, 10, len(data.x))  # We can safely access these keys now
        fig = go.Figure()

        units = {"Accel": "m/s²", "Gyro": "°/s"}

        for color, axis in zip(colors, [data.x, data.y, data.z]):
            y_data = np.array(axis)
            if label == "Gyro":
                y_data = np.rad2deg(y_data)

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_data,
                    mode="lines",
                    name=f"{label}-x",
                    line=dict(color=color),
                )
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=TUM_GREY_BG,
            plot_bgcolor=TUM_GREY_BG,
            xaxis_title="Time (s)",
            yaxis_title=f"{label} ({units[label]})",
            margin=dict(l=10, r=10, t=10, b=10),
            autosize=True,
        )
        return fig

    def create_layout(self) -> html.Div:
        """Create the layout of the Dash app."""
        return html.Div(
            style={
                "backgroundColor": TUM_GREY_BG,
                "color": TUM_BLUE,
                "height": "100vh",
                "width": "100vw",
                "overflow": "hidden",
                "margin": "0",
                "padding": "0",
            },
            children=[
                html.H2(
                    "IMU Dashboard", style={"textAlign": "center", "margin": "0.5rem"}
                ),
                dcc.Interval(
                    id="update-interval", interval=UPDATE_RATE_MILLISEC, n_intervals=0
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "height": "90%",
                        "width": "100%",
                    },
                    children=[
                        html.Div(
                            style={
                                "flex": "1",
                                "display": "flex",
                                "flexDirection": "column",
                                "width": "100%",
                                "height": "100%",
                            },
                            children=[
                                dcc.Graph(
                                    id="accel-plot",
                                    style={
                                        "flex": "1",
                                        "width": "100%",
                                        "height": "50%",
                                    },
                                ),
                                dcc.Graph(
                                    id="gyro-plot",
                                    style={
                                        "flex": "1",
                                        "width": "100%",
                                        "height": "50%",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            style={"flex": "1", "width": "100%", "height": "100%"},
                            children=[
                                dcc.Graph(
                                    id="orientation-plot",
                                    style={"width": "100%", "height": "100%"},
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

    def run(self) -> None:
        """Run the Dash server."""
        self.app.layout = self.create_layout()
        self.app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    start_imu_thread(device_name="CIRCUITPY", live_data=live_data)
    app = Dash(__name__)
    app.title = "IMU Dashboard"
    dashboard = DashboardApp(app=app, live_data=live_data)
    dashboard.run()
