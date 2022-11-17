-- ##数据
select response.tdbank_imp_date, response.media_app_id, response.position_id, response.creative_id,
    nvl(response.pltv, 0) as pltv,
    nvl(response.pctcvr, 0) as pctcvr,
    nvl(response.pctr, 0) as pctr,
    nvl(response.bid_price, 0) as bid_price,
    nvl(response.ecpm, 0) as response_ecpm,
    nvl(impression.win_price, 0) as win_price,
    nvl(loss_win.winner_bid_price, 0) as winner_bid_price,
    nvl(cli.click_num, 0) as click_num,
    nvl(act.target_cpa, 0) as target_cpa,
    nvl(pay.pay_amount, 0) as pay_amount
from (
    select tdbank_imp_date, request_id, media_app_id,
        position_id,
        get_json_object(algo_ext_info, '$.Pltv') as pltv,
        get_json_object(algo_ext_info, '$.ClickPcvr')*pctr + get_json_object(algo_ext_info, '$.ImpPctcvr') as pctcvr,
        pctr,
        creative_id,
        ecpm,
        get_json_object(algo_ext_info,'$.BidPrice') as bid_price
    from ieg_mms::yky_dsl_yky_dsp_bid_response_fht0
    where tdbank_imp_date between 2022102109 and 2022102120
        and is_test = 0 and app_id != 2 and service_env = 3
        and random_bid_flag != 2
        and media_platform_id = 80
        -- and media_app_id in (30797, 30796) -- 最右
        and media_app_id in (30391, 30390) -- QQ 浏览器
        and co_type = 1 -- 1=广告；2=联运；3=品牌广告
) response
left join(
    select
        request_id,
        creative_id,
        win_price
    from ieg_mms::yky_dsl_yky_dsp_impression_fht0
    where tdbank_imp_date between 2022102109 and 2022102120
        and is_valid = 1 and is_test = 0 and app_id != 2 and service_env = 3 and is_charge = 1
        and random_bid_flag != 2
        and media_platform_id = 80
        -- and media_app_id in (30797, 30796) -- 最右
        and media_app_id in (30391, 30390) -- QQ 浏览器
        and co_type = 1 -- 1=广告；2=联运；3=品牌广告
) impression
on response.creative_id = impression.creative_id and response.request_id = impression.request_id
left join(
    select request_id, creative_id, winner_bid_price
    from ieg_mms::yky_dsl_yky_dsp_win_fht0
    where tdbank_imp_date between 2022102109 and 2022102120
        and win_code <> 1
        and adn_id <> 0
        and winner_bid_price > 0
        and service_env=3
        and is_valid=1
        and is_test=0
        and app_id not in (2)
        and media_platform_id=80
        -- and media_app_id in (30797, 30796) -- 最右
        and media_app_id in (30391, 30390) -- QQ 浏览器
        and co_type=1
) loss_win
on response.creative_id = loss_win.creative_id and response.request_id = loss_win.request_id
left join (
    select distinct request_id, creative_id, 1 as click_num
    from ieg_mms::yky_dsl_yky_dsp_click_fht0
    where  tdbank_imp_date between 2022102109 and 2022102120
) cli on response.request_id = cli.request_id and response.creative_id = cli.creative_id
left join (
    select distinct request_id, creative_id,
    get_json_object(algo_ext_info,'$.BidPrice') as target_cpa
    from ieg_mms::yky_dsl_yky_dyeing_action_data_all_new_fht0
    where tdbank_imp_date between 2022102109 and 2022102120
        and action_type in (21, 41)
) act on response.request_id = act.request_id and response.creative_id = act.creative_id
left join (
    select request_id, creative_id,
        sum(pay_amount) as pay_amount,
        case when sum(pay_amount) > 64800 then 64800 else sum(pay_amount) end as truncated_pay_amount,
        count(1) as pay_cnt
    from ieg_mms::yky_dsl_yky_dyeing_action_data_all_new_fht0
    where tdbank_imp_date between 2022102109 and 2022102120
    and action_type = 51
    group by request_id, creative_id
) pay on response.request_id = pay.request_id and response.creative_id = pay.creative_id
WHERE response.tdbank_imp_date is not null
    and response.media_app_id is not null
    and response.position_id is not null
    and response.creative_id is not null
    -- and (nvl(impression.win_price, 0) <> 0 or nvl(loss_win.winner_bid_price, 0) <> 0)




