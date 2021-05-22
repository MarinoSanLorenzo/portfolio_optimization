import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import plotly.figure_factory as ff

__all__ = [
    "plot",
    "plot_low_high_prices",
    "plot_scatter_matrix",
    "plot_dist_returns",
    "plot_efficient_frontier",
    "plot_efficient_frontier_continuous_color",
    "plot_efficient_frontier_optimal_point",
    "plot_simulated_stocks",
]


def plot_simulated_stocks(
    data: pd.DataFrame,
    y,
    title=None,
    x="Date",
    label="simulation_name",
    line_shape="spline",
    render_mode="svg",
) -> plotly.graph_objects.Figure:
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=label,
        line_group=label,
        hover_name=label,
        line_shape=line_shape,
        render_mode=render_mode,
    )


def plot_efficient_frontier_continuous_color(
    portfolios_simulated: pd.DataFrame,
) -> None:
    return px.scatter(
        portfolios_simulated,
        x="volatility",
        y="returns",
        color="sharpe_ratio",
        title="Efficient Frontier - Sharpe Ratio shaded",
        color_continuous_scale=px.colors.diverging.RdYlGn
        # color_continuous_scale=px.colors.diverging.RdYlGn[::-1]
    )


def plot_efficient_frontier_optimal_point(portfolios_simulated: pd.DataFrame) -> None:
    max_ratio_idx = portfolios_simulated.sharpe_ratio.idxmax()
    portfolios_simulated["optimal"] = "No"
    portfolios_simulated.loc[max_ratio_idx, "optimal"] = "Yes"
    return px.scatter(
        portfolios_simulated,
        x="volatility",
        y="returns",
        color="optimal",
        title="Efficient Frontier - Optimal Point",
    )


def plot_efficient_frontier(
    portfolios_simulated: pd.DataFrame,
) -> plotly.graph_objects.Figure:
    return px.scatter(
        portfolios_simulated, x="volatility", y="returns", title="Efficient Frontier"
    )


def plot_dist_returns(
    stock_data_returns: pd.DataFrame, params: dict
) -> plotly.graph_objects.Figure:
    hist_data = [
        stock_data_returns.query(f'stock_name=="{stock}"')["returns"]
        for stock in params.get("STOCKS_INFO")
    ]
    group_labels = [stock for stock in params.get("STOCKS_INFO")]
    try:
        fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
    except ValueError:
        for data in hist_data:
            data.dropna(inplace=True)
        fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
    return fig


def plot_scatter_matrix(
    data: dict, params: dict, variable: str
) -> plotly.graph_objects.Figure:
    title = f"Scatter Matrix for {variable} Prices"
    components = pd.concat(
        [
            data.query(f'stock_name=="{stock_name}"')[variable]
            for stock_name in params.get("chosen_stocks")
        ],
        axis=1,
    )
    components.columns = [
        f"{stock.capitalize()}" for stock in params.get("chosen_stocks")
    ]
    return px.scatter_matrix(components, title=title)


def add_trace_high_low(
    fig: plotly.graph_objects.Figure, df: pd.DataFrame
) -> plotly.graph_objects.Figure:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.High,
            name="High",
            line=dict(color="firebrick", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df.Low,
            name="Low",
            line=dict(color="royalblue", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df.Open, name="Open", line=dict(color="firebrick", width=1)
        )
    )
    return fig


def plot_low_high_prices(
    df: pd.DataFrame, stock_name: str
) -> plotly.graph_objects.Figure:
    df = df.query(f'stock_name=="{stock_name}"')
    fig = go.Figure()
    # Create and style traces
    fig = add_trace_high_low(fig, df)
    # Edit the layout
    fig.update_layout(
        title=f"Average High, Low and Open Prices for the {stock_name} stock",
        xaxis_title="Date",
        yaxis_title="Prices",
    )
    return fig


def plot(
    data: pd.DataFrame,
    y,
    title=None,
    x="Date",
    label="stock_name",
    line_shape="spline",
    render_mode="svg",
) -> plotly.graph_objects.Figure:
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=label,
        line_group=label,
        hover_name=label,
        line_shape=line_shape,
        render_mode=render_mode,
    )
