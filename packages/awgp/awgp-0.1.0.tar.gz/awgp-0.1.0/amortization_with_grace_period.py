def awgp():
  import sys

  import pandas as pd

  loan = eval ( input ('貸款金額：') )   # loan amount

  yr = eval ( input ('年利率： 例如：8%, 請輸入 0.08 ') )     

  n = eval ( input ('貸款年數：') )

  limit = eval ( input ('只還利息不還本的寬限期, 以年為單位：') )

  mr = round(yr / 12, 5)   # 月利率

  mn = n * 12   # 月數

  m_limit = limit * 12   # 月數

  if limit >= n/1.9:

      print('只還利息不還本的寬限期不能大於', n/2, '年 !!!')

      sys.exit()

  repayment_monthly = 0

  list01 = []; list02 = []; list03 = []; list04 = []

  for i in range(1, m_limit+1):

      if i == 1:

          capital_balance = loan

          repay_interest_monthly = round(capital_balance * mr, 0)

          repay_capital_interest_monthly = repay_interest_monthly        

          list01.append(i) 

          list02.append(repayment_monthly)

          list03.append(repay_interest_monthly)

          list04.append(repay_capital_interest_monthly)

      else:

          capital_balance = capital_balance - repayment_monthly

          repay_interest_monthly = round(capital_balance * mr, 0)                 

          repay_capital_interest_monthly = repay_interest_monthly

          list01.append(i) 

          list02.append(repayment_monthly)

          list03.append(repay_interest_monthly)

          list04.append(repay_capital_interest_monthly)

  ml =  mn - m_limit   # 本息平均攤還法 (即本息定額攤還法), 計算出貸款本金償還所剩餘的期數

  repay_rate = (((1 + mr) ** ml) * mr) / (((1 + mr) ** ml) - 1)  # average repayment rate

  repayment_monthly = round(loan * repay_rate, 0)   # repay capital & interest

  for j in range(m_limit+1, mn+1):

      capital_balance = capital_balance - repayment_monthly

      if j != mn:            

          repay_interest_monthly = round(capital_balance * mr, 0)

      else:

          repay_interest_monthly = 0

      repay_capital_monthly = round(repayment_monthly - repay_interest_monthly, 0)

      list01.append(j) 

      list02.append(repay_capital_monthly)

      list03.append(repay_interest_monthly)

      list04.append(repayment_monthly)       

  dataset = {

      '攤還期數': list01,

      '每月應還本金金額': list02,

      '每月應付利息金額': list03,

      '每月應付本息金額': list04

      }

  pd.set_option('display.unicode.ambiguous_as_wide', True)  #欄位資料對齊

  pd.set_option('display.unicode.east_asian_width', True)  #欄位資料對齊

  pd.set_option('display.width', 150)    #設定輸出寬度

  df = pd.DataFrame(dataset)

  return print(df)

awgp()