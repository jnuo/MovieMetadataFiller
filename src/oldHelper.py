def get_all_dates():
    dates = []

    for i in googleSpending.keys():
        try:
            b = dates.index(i)
        except:
            dates.append(i)
    for i in googleSC.keys():
        try:
            b = dates.index(i)
        except:
            dates.append(i)
    return dates

def get_google_spending():
    googleSpendingFileName = 'GoogleSpendings.xlsx'
    director = os.path.dirname(__file__) + "/docs/"
    path = director + googleSpendingFileName
    wb = load_workbook(path)

    sheet = wb['Sheet1']
    row_count = sheet.max_row
    column_count = sheet.max_column

    googleCost: dict[str, float] = {}

    i = 2
    while i <= row_count:
        indexDate = "A" + str(i)
        indexCost = "B" + str(i)
        cell = sheet[indexDate].value
        valueDate = ""
        try:
            valueDate = str(cell.strftime("%Y-%m-%d"))
        except:
            continue

        valueCost = sheet[indexCost].value
        if valueDate not in googleCost:
            googleCost[valueDate] = valueCost
        i = i + 1

    return googleCost


def getGoogleSC():
    googleProfitFileName = 'GoogleProfits.xlsx'
    director = os.path.dirname(__file__) + "/docs/"
    path = director + googleProfitFileName
    wb = load_workbook(path)

    sheet = wb['Sheet1']
    row_count = sheet.max_row
    column_count = sheet.max_column

    googlesc: dict[str, float] = {}

    i = 2
    while i <= row_count:
        indexDate = "A" + str(i)
        indexProfit = "B" + str(i)
        cell = sheet[indexDate].value
        valueDate = ""
        try:
            valueDate = str(cell.strftime("%Y-%m-%d"))
        except:
            continue

        valueCost = sheet[indexProfit].value
        if valueDate not in googlesc:
            googlesc[valueDate] = valueCost
        i = i + 1

    return googlesc


def calculateRoi(dates, costs, profits):
    rois: dict[str, float] = {}
    cost = 0
    profit = 0
    roi = 0
    for i in dates:
        if i in costs:
            cost = costs[i]
        else:
            rois[i] = "-"
            continue
        if i in profits:
            profit = profits[i]
        else:
            rois[i] = "-"
            continue
        roi = float(profit / cost)
        rois[i] = roi

    return rois
