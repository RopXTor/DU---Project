import view
import repository

def main():
    
    config = repository.get_config()
    
    Fund_Stocks, end_date = view.get_inputs(config)
    
    view.display_info(config)
    view.display_plot_index(Fund_Stocks, end_date, config)
    view.display_info_fund(Fund_Stocks, config)
    view.display_plot(Fund_Stocks, end_date, config)
    view.display_stat(Fund_Stocks, end_date, config)

if __name__ == "__main__":
    main()