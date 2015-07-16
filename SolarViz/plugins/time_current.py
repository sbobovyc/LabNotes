def plot(data):
    time_zero = float(data.get_data()[0]["timestamp"]) 
     
    # plot time vs. voltage
    stride = 10
    title = "Time vs. Current"
    xlabel = "time (s)"
    ylabel = "current (A)"
    xdata = "timestamp"
    ydata = "current"
    xfunction = xfunction=(lambda x: float(x) - time_zero)
    yfunction = None
    
    return data.get_data(), stride, title, xlabel, ylabel, xdata, ydata, xfunction, yfunction
                               
     
           
        

