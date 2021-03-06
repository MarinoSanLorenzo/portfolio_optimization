import pandas as pd
import dash_html_components as html
from dash_main import app
from src.frontend.callbacks import *
from src.frontend.plots import *
from src.constants import params
from src.utils import *
from src.frontend.layout import *
from src.frontend.components import *
from src.portfolio_optimization import *


#TODO:check portfolio property and variance function when changing the number of portfolio
params = get_user_inputs(params)


def main():
    ###########################################################
    #################       BACKEND                  #################
    ###########################################################


    chosen_stocks = params.get('chosen_stocks')

    investment_data = get_investment_data(params)
    your_investment_data = investment_data[investment_data.name.isin(chosen_stocks)]
    data_step0 = get_data(params)
    data_step1 = process_data(data_step0, params)
    covariance_tbl = get_covariance_tbl(data_step1)
    correlation_tbl = get_correlation_tbl(data_step1)
    portfolio_properties = get_portfolio_properties(data_step1, params)
    yearly_returns = get_returns(data_step1)
    volatility_yearly = get_volatility_yearly(data_step1)

    portfolio_info = pd.merge(
        portfolio_properties.share_allocation_df,
        yearly_returns,
        how="left",
        on="stock_name",
    )
    portfolio_info = pd.merge(
        portfolio_info, volatility_yearly, how="left", on="stock_name"
    )

    data_step2 = get_stock_data_returns(data_step1, params)

    portfolios_simulated = run_portfolios_simulations(
        data_step1, params
    )



    optimal_portfolio = get_portfolio_with(
        portfolios_simulated,
        lowest_volatility=True,
        highest_return=True,
        pretty_print_perc=False,
    )

    params["data_range"] = get_data_range(data_step2, params)
    sim = get_simulations(data_step2, optimal_portfolio, params)

    summary_msg = get_investment_summary(portfolios_simulated, sim, params)

    data = data_step2

    ###########################################################
    #################         FRONTEND                #################
    ###########################################################

    params["data"] = data
    params["data_range"] = get_data_range(data, params)
    params["your_investment_data"] = get_data_table(your_investment_data)
    params["open_prices_plot_all"] = plot(data, "Open", "Open prices")
    params["open_prices_plot_lst"] = add_layout_components_for_multiple_plots(
        plot_low_high_prices, data, params
    )
    params["covariance_tbl_dt"] = get_data_table(covariance_tbl)
    params["correlation_tbl_dt"] = get_data_table(
        correlation_tbl, pretty_print_perc=True
    )
    params["open_scatter_matrix"] = plot_scatter_matrix(data, params, "Open")
    params[
        "default_portfolio_variance"
    ] = portfolio_properties.variance_portfolio_return
    params["default_portfolio_expected_return"] = "{:.2%}".format(
        portfolio_properties.expected_portfolio_return
    )
    params["portfolio_info_dt"] = get_data_table(portfolio_info, pretty_print_perc=True)
    params["dist_returns_plot"] = plot_dist_returns(data, params)
    params[
        "efficient_frontier_optimal_point_plot"
    ] = plot_efficient_frontier_optimal_point(portfolios_simulated)
    params[
        "efficient_frontier_continuous_color_plot"
    ] = plot_efficient_frontier_continuous_color(portfolios_simulated)

    params["portfolios_simulated_dt"] = get_data_table(
        portfolios_simulated, pretty_print_perc=True
    )
    params["summary_msg"] = summary_msg
    params[
        "simulated_stock_plots_lst"
    ] = add_layout_compoment_for_simulated_stock_plots(data, sim.simulated_stocks)
    params["simulations_optimal_portfolio_plot"] = plot_simulated_stocks(
        sim.simulations_optimal_portfolio_df,
        y="Adj Close Price simulated",
        title="Optimal Portfolio simulations",
    )

    params['investment_data_component'] =  html.Ul(
        children=[html.Li(f"{k}:\t{v}") for k, v in params.items() if k in params.get('params_to_show')]
    )
    app.layout = get_layout(params)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
