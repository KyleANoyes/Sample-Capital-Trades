from datetime import datetime
from datetime import date
import csv
import yfinance as yf

def data_r(member):
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_trades\{member}_trades.csv"
    try:
        file = open(member, "r")
        file.close()
    except:
        file = open(member, "x")
        file.close()

    with open(member, "r") as fp:
        trades = fp.readlines()
        trades_len = len(trades)
        fp.close()
        return trades, trades_len

def data_r_perf(member):
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_performance\{member}_performance.csv"
    try:
        file = open(member, "r")
        file.close()
    except:
        file = open(member, "x")
        file.close()

    with open(member, "r") as fp:
        trades = fp.readlines()
        trades_len = len(trades)
        fp.close()
        return trades

def data_w(new_data, member):
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_trades\{member}_trades.csv"
    with open(member, 'a', newline= "") as append:
        database = csv.writer(append)
        database.writerow(new_data)
        append.close()

def error(element):
    member = "error_log.txt"
    try:
        file = open(member, "r")
        file.close()
    except:
        file = open(member, "x")
        file.close()

    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    data = open("error_log.txt", "r")
    database = data.read()
    data.close()
    entry = F"{dt_string} - Get {element} has reported an error\n"
    database = database + entry
    with open(member, 'w') as f:
        for item in database:
            f.write(item)
    f.close()

def position(new_data, member):
    member_g = (member)
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_positions\{member_g}_positions.csv"
    try:
        file = open(member, "r")
        file.close()
    except:
        file = open(member, "x")
        file.close()
    
    with open(member, "r") as fp:
        trades = fp.readlines()
        trades_len = len(trades)
        fp.close()
    
    new_entry = F"{str(new_data[2])},{str(new_data[3])},{str(new_data[4])},{str(new_data[5])}"
    #new_data = [date, pub_date, ticker, action, volume, price]
    i = 0
    j = -1
    while True:
        if trades_len == 0:
            break
        elif str(new_data[2]) in str(trades[j]):
            trades_stock = str(trades[j])
            trades_stock = trades_stock.split(",")
            if str(new_data[2]) == str(trades_stock[0]) and float(trades_stock[3]) != 0:
                i = 1
                break
            elif (j * - 1) == int(trades_len):
                i = 0
                break
            else:
                j = j - 1
                continue
        elif (j * - 1) == int(trades_len):
            i = 0
            break
        else:
            j = j - 1
            continue
    if i == 1:
        ltrade = str(trades[j])
        ltrade = ltrade.split(",")
        pchange = float(new_data[5]) / float(ltrade[3])
        pchange = round(pchange, 2)
        bvalue = float(ltrade[4])
        if bvalue != 0:
            nvalue = float(ltrade[2]) * pchange
            performance = nvalue / bvalue
            performance = round(performance, 2)
            if str(new_data[3]) == "buy":
                bvalue = bvalue + float(new_data[4])
                nvalue = nvalue + float(new_data[4])
            else:
                bvalue = bvalue - float(new_data[4])
                nvalue = nvalue - float(new_data[4])
            #new_data = [date, pub_date, ticker, action, volume, price]
            if bvalue <= 0 or nvalue <= 0:
                bvalue = float(new_data[4])
                nvalue = float(new_data[4])
            new_data = F"{str(new_data[2])},{str(new_data[3])},{str(nvalue)},{str(new_data[5])},{str(bvalue)},{str(performance)},{str(new_data[0])}\n"
            
            member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_positions\{member_g}_positions.csv"
            f_object = open(member, "a")
            f_object.write(str(new_data))
            f_object.close()
            return 0
    else:
        if "sell" in str(new_data[3]):
            return 1
        else:
            bvalue = new_data[4]
            new_data = F"{str(new_entry)},{str(bvalue)},1,{str(new_data[0])}\n"
            member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_positions\{member_g}_positions.csv"
            f_object = open(member, "a")
            f_object.write(str(new_data))
            f_object.close()
            return 0

def value(member):
    member_g = member
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_positions\{member_g}_positions.csv"
    try:
        file = open(member, "r")
        file.close()
    except:
        file = open(member, "x")
        file.close()
    with open(member, "r") as fp:
        position = fp.readlines()
        position_len = len(position)
        fp.close()
    
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_performance\{member_g}_performance.csv"
    file = open(member, "w")
    file.close()

    stocks = ""
    date_track = ""
    perf_total_gain_top = 0
    perf_total_loss_top = 0
    perf_total_gain_base = 0
    perf_total_loss_base = 0
    if position_len > 0:
        for i in range(position_len):
            date_all = ""
            adjusted_value = 0
            base_value = 0
            record_start = 0
            bottom = 0
            top = 0
            position_data = position[i]
            position_data = str(position_data)
            position_data = position_data.split(",")
            ticker = position_data[0]
            date_track += str(position_data[6]) 
            ticker_check = ticker + ","
            
            if ticker_check in stocks:
                pass
            else:
                stocks += ticker + ","
                for i in range(position_len):
                    position_l = position[i]
                    position_l = str(position_l)
                    position_l = position_l.split(",")
                    if str(ticker) == str(position_l[0]):
                        adjusted_value = (float(position_l[2]) - float(position_l[4]) + float(position_l[2]))
                        base_value = float(position_l[4])
                        date_all += position_l[6]
                        if adjusted_value == 0:
                            top += base_value
                            bottom += base_value
                        else:
                            top += adjusted_value
                            bottom += base_value
                        if record_start == 0:
                            record_start = position_l[6]
                        else:
                            pass
                    else:
                        pass
                if bottom != 0 and top != 0:
                    dates = date_all.split("\n")
                    date_1 = str(dates[0])
                    date_1_record = date_1
                    date_1 = date_1.split("-")
                    date_1_y = int(date_1[0])
                    date_1_m = int(date_1[1])
                    date_1_d = int(date_1[2])
                    date_2 = str(dates[-2])
                    date_2_record = date_2
                    date_2 = date_2.split("-")
                    date_2_y = int(date_2[0])
                    date_2_m = int(date_2[1])
                    date_2_d = int(date_2[2])

                    d0 = date(date_1_y, date_1_m, date_1_d)
                    d1 = date(date_2_y, date_2_m, date_2_d)
                    delta = d1 - d0
                    if delta.days == 0:
                        delta = 1
                    else:
                        delta = delta.days

                    pos_perf = top / bottom
                    
                    gain_loss = top - bottom
                    gain_loss = round(gain_loss, 3)
                    score_m = (pos_perf - 1) / (delta / 30) + 1
                    score_m = round(score_m, 3)
                    score_y = (pos_perf - 1) / (delta / 365) + 1
                    score_y = round(score_y, 3)
                    pos_perf = round(pos_perf, 3)
                    bottom = round(bottom, 3)
                    if float(gain_loss) > 0 and pos_perf < 10:
                        record_gain = F"{str(ticker)},{str(pos_perf)},{str(gain_loss)},{str(score_m)},{str(score_y)},{str(date_1_record)},{str(date_2_record)}\n"
                        perf_total_gain_top += (gain_loss * pos_perf)
                        perf_total_gain_base += gain_loss
                        member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_performance\{member_g}_performance.csv"
                        f_object = open(member, "a")
                        f_object.write(str(record_gain))
                        f_object.close()
                    else:
                        if pos_perf < 10:
                            record_loss = F"{str(ticker)},{str(pos_perf)},{str(gain_loss)},{str(score_m)},{str(score_y)},{str(date_1_record)},{str(date_2_record)}\n"
                            gain_loss = gain_loss * (-1)
                            perf_total_loss_top += (gain_loss * pos_perf)
                            perf_total_loss_base += gain_loss
                            member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_performance\{member_g}_performance.csv"
                            f_object = open(member, "a")
                            f_object.write(str(record_loss))
                            f_object.close()


        #perf_total_gain = perf_total_gain_top / perf_total_gain_base
        if perf_total_gain_base == 0:
            perf_total_gain_base = 1
            perf_total_gain = perf_total_gain_top / perf_total_gain_base
        else:
            perf_total_gain = perf_total_gain_top / perf_total_gain_base
        #perf_total_loss = perf_total_loss_top / perf_total_loss_base
        if perf_total_loss_base == 0:
            perf_total_loss_base = 1
            perf_total_loss = perf_total_loss_top / perf_total_loss_base
        else:
            perf_total_loss = perf_total_loss_top / perf_total_loss_base

        perf_total_top = (perf_total_gain_base * perf_total_gain) + (perf_total_loss_base * perf_total_loss)
        perf_total_base = (perf_total_gain_base + perf_total_loss_base)
        perf_total = perf_total_top / perf_total_base

        dates = date_track.split("\n")
        date_1 = str(dates[0])
        date_1_record = date_1
        date_1 = date_1.split("-")
        date_1_y = int(date_1[0])
        date_1_m = int(date_1[1])
        date_1_d = int(date_1[2])
        date_2 = str(dates[-2])
        date_2_record = date_2
        date_2 = date_2.split("-")
        date_2_y = int(date_2[0])
        date_2_m = int(date_2[1])
        date_2_d = int(date_2[2])

        d0 = date(date_1_y, date_1_m, date_1_d)
        d1 = date(date_2_y, date_2_m, date_2_d)
        delta = d1 - d0
        if delta.days == 0:
            delta = 1
        else:
            delta = delta.days

        score_m = (perf_total - 1) / (delta / 30) + 1
        score_m = round(score_m, 3)
        score_y = (perf_total - 1) / (delta / 365) + 1
        score_y = round(score_y, 3)
        perf_total_base = round(perf_total_base, 2)

        performance = F"{str(perf_total)},{str(score_m)},{str(score_y)},{str(perf_total_base)}"
        member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_performance\{member_g}_performance.csv"
        f_object = open(member, "a")
        f_object.write(performance)
        f_object.close()

#with open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\\active_members.txt", "r") as fp:
    #oof = fp.readlines()
#for i in range(len(oof)):
    #oof_i = oof[i].replace("\n", "")
    #try:
        #value(oof_i)
    #except:
        #pass

def total_performance(all_name):
    member_performance = str("D:\Dropbox\\2022\Python Master\Capitol Trades\Congressional_Performance.csv")
    file = open(member_performance, "w")
    file.close()

    with open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\spy.txt") as f:
        spy = float(f.read())
        f.close()

    top_portfolio = ""
    combined_top = 0
    combined_bottom = 0
    for i in range(len(all_name)):
        try:
            member = all_name[i]
            member_g = member
            data = data_r_perf(member)
            data_len = len(data)
            if len(data) > 1:
                #some data is not being generate correctly
                data = data[-1]
                data_final = data.split(",")
                data_perf = data_final[1]
                if float(data_perf) > spy:
                    top_portfolio += all_name[i] + ","
                data_value = data_final[-1]
                if float(data_perf) >= 0:
                    combined_top += (float(data_perf) * float(data_value))
                    combined_bottom += float(data_value)
                else:
                    combined_top += ((float(data_perf) * float(data_value)) * -1)
                    combined_bottom += (float(data_value) * -1)
                data_perf_y = round(((float(data_perf) - 1) * 12.166), 3)
                data_perf_y = (abs(data_perf_y) + 1)
                data_value = round(float(data_value), 0)
                if float(data_value) == 2:
                    data_perf = 1
                    data_perf_y = 1
                    data_value = 1
                member_title = member_g.replace("_", " ")
                member_title = member_title.title()
                performance = F"{str(member_title)},{str(data_perf)},{str(data_perf_y)},{str(data_value)}\n"
                f_object = open(member_performance, "a")
                f_object.write(str(performance))
                f_object.close()
        except:
            pass
    total_perf = combined_top / combined_bottom
    total_perf_m = round(total_perf, 3)
    total_perf_y = round(((float(total_perf) - 1) * 12.166), 3)
    total_perf_y = (abs(total_perf_y) + 1)
    performance = F"Weighted Avg,{str(total_perf_m)},{str(total_perf_y)}\n"
    f_object = open(member_performance, "a")
    f_object.write(str(performance))
    f_object.close()

    top_portfolio = top_portfolio[0:-1]
    top_portfolio = top_portfolio.split(",")
    top_members(top_portfolio)

#with open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\\active_members.txt", "r") as fp:
    #all_names = fp.read()
    #all_names = all_names.split("\n")
#total_performance(all_names)

def top_members(top_portfolio):
    today = datetime.today()
    today = datetime.today().strftime("%Y-%m-%d")
    with open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\\top_members.txt", "r") as fp:
        active_members = fp.read()
        member_list = ""
        active_members = active_members.replace("\n", ",")
        active_members = active_members[0:-1]
        active_members = active_members.split(",")
        active_members_name = active_members[0::2]
        active_members_date = active_members[1::2]
        fp.close()

    # Need to recreate member_list with confimred members. Current list is just being apended
    for i in range(len(active_members_name)):
        if active_members_name[i] in str(top_portfolio):
            member_list += F"{active_members_name[i]},{active_members_date[i]}\n"
        else:
            pass
    for i in range(len(top_portfolio)):
        if top_portfolio[i] in member_list:
            pass
        else:
            member_list += F"{top_portfolio[i]},{today}\n"
    for i in range(len(active_members_name)):
        if active_members_name[i] in member_list:
            pass
        else:
            removal(active_members_name[i], active_members_date[i])
    text_top = open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\\top_members.txt", "w")
    text_top.write(member_list)
    text_top.close()


def removal(member, add_date):
    member_g = (member)
    member = F"D:\Dropbox\\2022\Python Master\Capitol Trades\\all_positions\{member_g}_positions.csv"
    with open(member, "r") as fp:
        trades = fp.readlines()
        fp.close()
    for i in range(len(trades)):
        len(trades)
        entry = str(trades[len(trades) - i - 1])
        entry = entry.replace("\n", "")
        entry = entry.split(",")
        entry_d = entry[-1]
        if entry_d >= add_date:
            stock = entry[0]
            position = float(entry[2])
            price = float(entry[3])
            price_current = yf.Ticker(stock.upper()).history("1m")["Close"].values[0]
            price_current = round(price_current, 3)
            gainloss = price_current / price
            trade = position * gainloss
            trade = round(trade, 3)
            market_order = F"{stock},sell,{trade}\n"
            f_object = open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\market_orders.txt", "a")
            f_object.write(str(market_order))
            f_object.close()
            today = datetime.today().strftime("%Y-%m-%d")
            market_order = F"{stock},sell,{trade},{today}\n"
            f_object = open("D:\Dropbox\\2022\Python Master\Capitol Trades\maintenance\\audit.txt", "a")
            f_object.write(str(market_order))
            f_object.close()
        else:
            break
            

def main(active_members):
    for i in range(len(active_members)):
        member = active_members[i]
        data = data_r(member)
        data = data[0]
        try:
            value(member)
        except:
            pass
    total_performance(active_members)

def entry_valid(new_data, member):
    trades_source, lines = data_r(member)
    lines = lines - 1
    repeat = 0
    new_data_pub = new_data[0]
    new_data = F"{str(new_data[1])},{str(new_data[2])},{str(new_data[3])},{str(new_data[4])}\n"
    for i in range(lines):
        trades = trades_source[lines - i]
        trades = str(trades)
        trades = trades.split(",")
        trades_pub = trades[0]
        trades = F"{str(trades[1])},{str(trades[2])},{str(trades[3])},{str(trades[4])}\n"
        if trades_pub[0] > new_data_pub[0]:
            repeat = repeat
            break
        elif str(new_data) == str(trades):
            repeat = 1
            break
        else:
            repeat = repeat
        i = i + 1
    return repeat