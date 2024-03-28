def dcf(coc,roce,gdhgp,tgr,fp,hgp):
    tax_rate = 0.25
    coc = coc/100
    roce = roce/100
    roce = roce * (1-tax_rate)
    gdhgp = gdhgp/100
    tgr = tgr/100
    rr1 = gdhgp/roce
    rr2 = tgr/roce
    cap_emp = 100
    prev_cap_emp = 100
    egr = 0
    nopat = 0
    prev_nopat = 0
    investment = 0
    fcf = 0
    disc_factor = 0
    disc_fcf = 0
    disc_fcf_li = []
    init_nopat = 0
    #High Growth Period formulas
    #Earnings growth rate = (nopat(i)/prev_nopat(i-1)-1) for i>=1
    #NOPAT = Prev_Cap * roce
    #Cap_Emp = Prev_Cap_Emp + Investment
    #Investment = NOPAT*RR1
    #FCF = NOPAT - Investment
    #Disc_Factor = 1/(1+coc)**i
    #Disc_fcf = fcf*disc_factor
    for i in range(hgp+1):
        if(i>0):
            egr = (nopat/prev_nopat) - 1
            prev_nopat = nopat
        
        nopat = cap_emp*roce
        if(i==0):
            init_nopat = nopat
            prev_nopat = nopat
        prev_cap_emp = cap_emp
        investment = nopat * rr1
        cap_emp = cap_emp + investment
        fcf = nopat - investment
        disc_factor = (1/(1+coc))**i
        disc_fcf = fcf * disc_factor
        disc_fcf_li.append(disc_fcf)

    #Fade Growth period formulas
    #Earnings growth rate = prev_egr-(gdhgp-tgr)/fp
    #Investment = next_egr/roce*nopat
    #Rest of them are same as High Growth period
    next_egr = 0
    for i in range(hgp+1,hgp+fp+1):
        egr = egr-((gdhgp-tgr)/fp)
        #next_egr = egr-((gdhgp-tgr)/fp)
        nopat = cap_emp*roce

        investment = (egr/roce)*nopat
        cap_emp = cap_emp + investment
        fcf = nopat - investment
        disc_factor = (1/(1+coc))**i
        disc_fcf = fcf * disc_factor
        disc_fcf_li.append(disc_fcf)
    terminal_nopat = (nopat*(1+tgr))/(coc-tgr)
    terminal_investment = terminal_nopat*rr2
    terminal_fcf = terminal_nopat - terminal_investment
    terminal_disc_factor = disc_factor
    terminal_disc_fcf = terminal_fcf * terminal_disc_factor
    disc_fcf_li.append(terminal_disc_fcf)
    intrinsic_val = sum(disc_fcf_li)
    calc_iPE = intrinsic_val/init_nopat
    return calc_iPE