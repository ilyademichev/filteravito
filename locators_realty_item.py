from selenium.webdriver.common.by import By


class Locators:
    #appartment
    APPARTMENT_A = (By.XPATH,"//a[contains(text(),'квартира')]")
    #load more items button
    LOAD_MORE_SPAN = (By.XPATH, "//span[contains(text(),'Загрузить еще')]")
    #time
    TIMESTAMP_ITEM_DIV = (By.XPATH, "//div[@data-marker='item-stats/timestamp']")
    TIMESTAMP_FILTER_DIV = (By.XPATH, "//div[@data-marker='item/datetime']")
    # price
    PRICE_SPAN = (By.XPATH, "//span[@data-marker='item-description/price']")
    # full address
    ADDRESS_SPAN = (By.XPATH, "//span[@data-marker='delivery/location']")
    # title of a company or an  owner
    COMPANY_SPAN = (By.XPATH, "//span[@data-marker='seller-info/postfix']")
    # name of a company or an owner contact name
    CONTACT_NAME_SPAN = (By.XPATH, "//span[@data-marker='seller-info/name']")
    # full text description
    DESCRIPTION_SPAN = (By.XPATH, "//div[@data-marker = 'item-description/text']")
    # area
    AREA_SPAN = (By.XPATH, "//div[@data-marker = 'item-properties-item(9)/description']")
    # floor
    FLOOR_SPAN = (By.XPATH, "//div[@data-marker = 'item-properties-item(4)/description']")
    # rooms
    NUMOF_ROOMS_SPAN = (By.XPATH, "//div[@data-marker = 'item-properties-item(8)/description']")
    # phone button link
    PHONE_POPUP_SHOW_LINK = (By.XPATH, "//a[@data-marker='item-contact-bar/call']")
    #    data-marker='item-contact-bar/call"
    # text phone number
    PHONE_TEXT = (By.XPATH, "//span[@data-marker='phone-popup/phone-number']")
    # exctract images' links by \u002F delimeter from embedded javascript
    SCRIPT_WITH_IMAGES_LINKS = (By.XPATH, "/html/body/script[1]")
    SIZEOF_IMAGE = '640x480'
    FORMATOF_IMAGE = '.jpg'

# extracted sample image link
#
# "640x480":"https:\u002F\u002F99.img.avito.st\u002F640x480\u002F7850203299.jpg
#
# script sample

# <script type="text/javascript">window.__initialData__ = {"geo":{"id":621540,"parentId":null,"hasChildren":false,"hasDirections":false,"hasMetro":false,"mode":"default","laas":false,"forcedByUser":false,"slug":"","names":{"1":"Россия","2":"России","6":"России"},"coords":{"lat":55.755814,"lng":37.617635},"showGeoBanner":true},'item":{"complementaryItems":null,"autotekaTeaserData":{"content":null,"isAutotekaTeaserFetch":false,"error":null},"domotekaTeaserData":{"content":null,"isDomotekaTeaserFetch":false,"error":null},"searchUrl":"","redirectUrl":null,"isFetch":false,"isError":false,'item":{"refs":{"locations":{"630270":{"name":"Калужская область"},"630530":{"name":"Обнинск","parentId":630270}},"categories":{"4":{"name":"Недвижимость"},"24":{"name":"Квартиры","parentId":4}}},"id":1838922216,"categoryId":24,"locationId":630530,"sharing":{"fb":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=fb&utm_medium=item_page_mavnew&utm_source=soc_sharing","gp":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=gp&utm_medium=item_page_mavnew&utm_source=soc_sharing","lj":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=lj&utm_medium=item_page_mavnew&utm_source=soc_sharing","mm":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=mm&utm_medium=item_page_mavnew&utm_source=soc_sharing","native":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=native&utm_medium=item_page_mavnew&utm_source=soc_sharing","ok":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=ok&utm_medium=item_page_mavnew&utm_source=soc_sharing","tw":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=tw&utm_medium=item_page_mavnew&utm_source=soc_sharing","vk":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216?utm_campaign=vk&utm_medium=item_page_mavnew&utm_source=soc_sharing","url":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216"},"coords":{"lat":55.147533,"lng":36.627449},"address":"Калужская область, Боровский р-н, д. Кабицыно, микрорайон Молодёжный, 3","geoReferences":[],"title":"1-к квартира, 38 м², 3\u002F4 эт.","titleGenerated":true,"userType":"company","time":1592047740,"description":"Продается 1-комн квартира в жилом и благоустроенном районе ЖК Молодежный д 3.\nВ квартире социальная отделка, требуется косметический ремонт. Вид из окна очень хороший  - во двор и  на детский сад.\nВ микрорайоне свои магазины, аптека, сетевой магазин \" Верный\",   муниципальный детский сад, игровые и спортивные площадки!\nПомощь в одобрении ипотеки за 1 день. Без торга. Без комиссий","parameters":{"flat":[{"title":"Категория","description":"Квартиры"},{"title":"Тип объявления","description":"Купить"},{"title":"Право собственности","description":"Собственник"},{"title":"Этаж","description":"3"},{"title":"Этажей в доме","description":"4"},{"title":"Тип дома","description":"Кирпичный"},{"title":"Вид объекта","description":"Вторичка"},{"title":"Количество комнат","description":"1-комнатные"},{"title":"Общая площадь, м²","description":"38"}],"groups":[]},"images":[{"640x480":"https:\u002F\u002F99.img.avito.st\u002F640x480\u002F7850203299.jpg","432x324":"https:\u002F\u002F99.img.avito.st\u002F432x324\u002F7850203299.jpg","240x180":"https:\u002F\u002F99.img.avito.st\u002F240x180\u002F7850203299.jpg","140x105":"https:\u002F\u002F99.img.avito.st\u002F140x105\u002F7850203299.jpg","100x75":"https:\u002F\u002F99.img.avito.st\u002F100x75\u002F7850203299.jpg"},{"640x480":"https:\u002F\u002F67.img.avito.st\u002F640x480\u002F7850202967.jpg","432x324":"https:\u002F\u002F67.img.avito.st\u002F432x324\u002F7850202967.jpg","240x180":"https:\u002F\u002F67.img.avito.st\u002F240x180\u002F7850202967.jpg","140x105":"https:\u002F\u002F67.img.avito.st\u002F140x105\u002F7850202967.jpg","100x75":"https:\u002F\u002F67.img.avito.st\u002F100x75\u002F7850202967.jpg"},{"640x480":"https:\u002F\u002F24.img.avito.st\u002F640x480\u002F7850200924.jpg","432x324":"https:\u002F\u002F24.img.avito.st\u002F432x324\u002F7850200924.jpg","240x180":"https:\u002F\u002F24.img.avito.st\u002F240x180\u002F7850200924.jpg","140x105":"https:\u002F\u002F24.img.avito.st\u002F140x105\u002F7850200924.jpg","100x75":"https:\u002F\u002F24.img.avito.st\u002F100x75\u002F7850200924.jpg"},{"640x480":"https:\u002F\u002F38.img.avito.st\u002F640x480\u002F7850201538.jpg","432x324":"https:\u002F\u002F38.img.avito.st\u002F432x324\u002F7850201538.jpg","240x180":"https:\u002F\u002F38.img.avito.st\u002F240x180\u002F7850201538.jpg","140x105":"https:\u002F\u002F38.img.avito.st\u002F140x105\u002F7850201538.jpg","100x75":"https:\u002F\u002F38.img.avito.st\u002F100x75\u002F7850201538.jpg"},{"640x480":"https:\u002F\u002F81.img.avito.st\u002F640x480\u002F7850203681.jpg","432x324":"https:\u002F\u002F81.img.avito.st\u002F432x324\u002F7850203681.jpg","240x180":"https:\u002F\u002F81.img.avito.st\u002F240x180\u002F7850203681.jpg","140x105":"https:\u002F\u002F81.img.avito.st\u002F140x105\u002F7850203681.jpg","100x75":"https:\u002F\u002F81.img.avito.st\u002F100x75\u002F7850203681.jpg"},{"640x480":"https:\u002F\u002F00.img.avito.st\u002F640x480\u002F7850207300.jpg","432x324":"https:\u002F\u002F00.img.avito.st\u002F432x324\u002F7850207300.jpg","240x180":"https:\u002F\u002F00.img.avito.st\u002F240x180\u002F7850207300.jpg","140x105":"https:\u002F\u002F00.img.avito.st\u002F140x105\u002F7850207300.jpg","100x75":"https:\u002F\u002F00.img.avito.st\u002F100x75\u002F7850207300.jpg"}],"price":{"title":"Цена","value":"1 650 000","metric":"руб."},"seller":{"title":"Частное лицо","name":"Собственник","manager":"Ольга","postfix":"Агентство","registrationTime":"На Авито с августа 2014","connection":{"title":"Подтверждён","sources":[{"type":"phone"},{"type":"email"}]},"link":"ru.avito:\u002F\u002F1\u002Fuser\u002Fprofile?userKey=0ad31dfdafb0806051abb5441a4df9ed&context=H4sIAAAAAAAAA0u0MrKqLgYSSpkpStaZVoYWxhaWRkZGhmbWxVbGVkrFRclKQJYJUL4kNVfJuhYAYDX-kzEAAAA","images":{"24x24":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_24x24.png","36x36":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_36x36.png","48x48":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_48x48.png","64x64":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_64x64.png","72x72":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_72x72.png","96x96":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_96x96.png","128x128":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_128x128.png","192x192":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_192x192.png","256x256":"https:\u002F\u002Fwww.avito.st\u002Fstub_avatars\u002F%D0%A1\u002F12_256x256.png"},"summary":"12 объявлений","userHashId":"51348688","online":false,"replyTime":{"category":3,"text":"Отвечает за несколько часов"},"isVerified":false,"subscribeInfo":{"isSubscribed":false},"userHash":"0ad31dfdafb0806051abb5441a4df9ed","registrationTimestamp":1407298942},"stats":{"views":{"today":44,"total":8125}},"contacts":{"list":[{"type":"phone","value":{"title":"Позвонить","uri":"ru.avito:\u002F\u002F1\u002Fphone\u002Fget?itemId=1838922216"}},{"type":"messenger","value":{"title":"Написать","uri":"ru.avito:\u002F\u002F1\u002Fitem\u002Fchannel\u002Fcreate?itemId=1838922216"}}]},"firebaseParams":{'itemID":"1838922216",'itemPrice":"1650000","withDelivery":"0","ne_posledniy_etazh":"Не последний","offer_type":"Продам","floor":"3","floors_count":"4","house_type":"Кирпичный","type":"Вторичка","area":"38 м²","rooms":"1","commission":"Собственник","userAuth":"0","isShop":"0","isASDClient":"0","vertical":"RE","categoryId":"24","categorySlug":"kvartiry","microCategoryId":"4929","locationId":"630530"},"needToCheckCreditInfo":true,"adjustParams":{"categoryId":"24","vertical":"RE","microCategoryId":"4929"},"needToCheckSimilarItems":true,"shouldShowDomotekaTeaser":true,"features":null,"icebreakers":{"texts":[{"id":3,"previewText":"Ещё продаёте?","messageText":"Здравствуйте! Ещё продаёте квартиру?"},{"id":2,"previewText":"Когда можно посмотреть?","messageText":"Здравствуйте! Когда можно посмотреть квартиру?"},{"id":26,"previewText":"Позвоните мне?","messageText":"Здравствуйте! Заинтересовала квартира, можете позвонить мне? Мой номер: +7"},{"id":31,"previewText":"Торг уместен?","messageText":"Здравствуйте! Скажите, торг уместен?"},{"id":1,"previewText":"Пришлёте видео?","messageText":"Здравствуйте! Можете показать на видео, как выглядит квартира?"},{"id":4,"previewText":"Покажете онлайн?","messageText":"Здравствуйте! Можете показать квартиру по видеосвязи?"}],"contact":"Спросите у продавца"},"seo":{"title":"1-к квартира, 38 м², 3\u002F4 эт. в Обнинске | Покупка и аренда квартир | Авито","description":"1-к квартира, 38 м², 3\u002F4 эт.. Объявления о продаже, покупке или аренде квартир в Обнинске на Авито. Продается 1-комн квартира в жилом и благоустроенном районе ЖК Молодежный д 3. В квартире социальная отделка, требуется косметический ремонт. Вид из окна очень хороший  - во двор и  на детский сад. В микрорайоне свои магазины, аптека, сетевой магазин \" Верный\",   муниципальный детский сад, игровые и спортивные площадки! Помощь в одобрении ипотеки...","canonicalUrl":"https:\u002F\u002Fwww.avito.ru\u002Fobninsk\u002Fkvartiry\u002F1-k_kvartira_38_m_34_et._1838922216"}},"timestamp":1592130233911,"modelSpecs":null,"isModelSpecsFetch":false},"favorite":{"favorites":{}},"favoriteSellers":{}} || {};
# window.__pluginsData__ = {"abCentral":{"ad_splitter":{"testGroup":"one","analyticParams":{"ab":"2089:1:0","defaultEvent":true}},"favourite_sellers_new_button_pp_ios":{"testGroup":"test","analyticParams":{"ab":"2656:1:8906","defaultEvent":true}},"favourite_sellers_new_button_pp_android":{"testGroup":"test","analyticParams":{"ab":"2658:1:3922","defaultEvent":true}},"favourite_sellers_new_button_item_android":{"testGroup":"test","analyticParams":{"ab":"2785:1:9796","defaultEvent":true}},"favourite_sellers_new_button_item_ios":{"testGroup":"test","analyticParams":{"ab":"2786:1:370","defaultEvent":true}},"favourite_sellers_share_block_item_android":{"testGroup":"move_out","analyticParams":{"ab":"2855:1:4869","defaultEvent":true}},"favourite_sellers_share_block_item_ios":{"testGroup":"move_out","analyticParams":{"ab":"2856:1:4052","defaultEvent":true}},"html_chunked":{"testGroup":"test_prioritized","analyticParams":{"ab":"3262:4:6012","defaultEvent":true}}},"mobileInfo":{"os":"AndroidOS","version":null,"mobile":"UnknownMobile","phone":null,"tablet":null,"bot":false,"crawler":false},"toggles":{"yartb":"1","yaasync":"","dfp":"1","criteo_targeting":"1","ad_fox":"1","ga":"1","gtm":"1","tns":"1","comscore":"1","criteo":"1","weborama":"1","yandex":"1","ya_webvisor":"1","yamaps":"1","share":"1","kagent":"1","verify_landline_tolfree":"","sendout_main_page":"1","sendout_other_page":"1","fingerprint":"1","firewall":"0","jslog_sentry":"1","adv_weborama_pixel_desktop_percentage":"1","adv_weborama_pixel_mav_percentage":"1","rmpAll":"1","rmpDesktop":"1","rmpMobile":"1","rmpApp":"1","rmpAndroid":"1","rmpIos":"1","rmpProbabilityAll":"100","rmpProbabilityDesktop":"100","rmpProbabilityMobile":"100","rmpProbabilityAndroid":"100","rmpProbabilityIos":"100","autoVasProbabilityCrownSign":"100","rewrite_bivrost_views":"1","stat_in_api_for_legacy_vas":"100","use_databus_for_get_stats":"1","rec_user_interests_percentage":"100","weborama_desktop_pixel_percentage":"100","weborama_mav_pixel_percentage":"100",'item_get_data_metric":"1","service_core_soa_metric":"1","ssr_client_compression":"lz4","adv_analytic_events_desktop_sampling_percentage":"1","adv_analytic_events_mav_sampling_percentage":"1","adv_analytic_events_apps_sampling_percentage":null,"adv_user_interests_sampling":"40","adv_enable_adfox_on_mobile_serp":"1","adv_bxc_cache_enable_write":"1","adv_bxc_cache_enable_read":"1","stories_story_1_enabled":"1","stories_story_2_enabled":null,"stories_story_3_enabled":"0","stories_story_4_enabled":"0","stories_story_5_enabled":"0","stories_story_6_enabled":"1","stories_story_7_enabled":null,"stories_story_8_enabled":"0","stories_story_9_enabled":"1","stories_story_10_enabled":"0","stories_story_11_enabled":"0","stories_story_12_enabled":"1","stories_story_13_enabled":"1","stories_story_14_enabled":"1","stories_story_15_enabled":"1","stories_story_16_enabled":"0","stories_story_17_enabled":null,"android_stories_send_clickstream":"100","ios_stories_send_clickstream":"100","mav_stories_send_clickstream":"100","service_user_antihack_switcher":"1","serviceAvatarEnabled":null,"recaptchaEnabled":"1","publicProfileSummaryPercentage":"100","publicProfileItemsCacheTime":"10","user_service_usage":"0","shop_manager_callback_off":"0","serpTrafficPercentage":"100","serpDeep":"3000","iskalo_log_region_stat":"1","sgPercentK8S":"0","sg_enable_sort_time":"0","sg_vips_weak":"1","sg_back_to_legacy_geo_filters":"0","delivery_witcher_pos_force":"1","delivery_witcher_pos_force_ios":"1","witcher_web_delivery_enabled":"1","witcher_web_regions_enabled":"1",'item_delivery":"1","delivery_toggle_al_1413":"1","delivery_toggle_al_1126":"1","delivery_toggle_al_4602":"1","delivery_toggle_warning":"0",'item_str":"1","str_toggle_str_692":"1","str_user_white_list":"76775988,114858270,87135488,84391317,77803377,89919146,98859861,39611836,217972,23744349,1709767,4673060,93318525,9960089,25121247,48751170,2747879,5021319,70222446,33586458,88801814,26242837,70843906,493893","analytics_b2b_hub_transport":"1","analytics_b2b_hub_realestate":false,"analytics_b2b_hub_job":"1","analytics_b2b_hub_general":"1","analytics_b2b_hub_services":false,"promo_b2b_hub_realestate":"1","promo_b2b_hub_job":"1","promo_b2b_hub_general":"1","promo_b2b_hub_services":true,"promo_b2b_hub_media":false,"advice_b2b_hub":"1","webim_b2b_hub":"1","b2b_hub_show_calendar_menu_item":"1","b2b_hub_redirect_to_new_tariffs_landing":"1","ct_provider_mtt":"1","ct_provider_mts":null,"ct_enable_hierarchy":"1",'item_description_show_watermark_probability":"100","csp_header_enabled_probability":"0","use_special_images_host":"1","suggest_service_enable_logs":"","phoneServiceProbability":null,"split_test_service":"100","service_ir":"1","geoProbability":"100","notification_settings_enabled":"1","service_moderation_callqueue_add_item_switch":"1","notification_reject_enabled":"0","notification_block_enabled":true,"moderation_doubles_grouping":"1","moderation_write_browser_info_to_service":true,"service_item_clone":"1","ldap_switch":null,"vpn_switch":"1","yandex_webvisor_switch":false,"snippet_iva_percentage":"1","snippet_iva_toggle":false,"new_backoffice_auth_percentage":"100","new_backoffice_permissions_check_percentage":"100","new_backoffice_permissions_read_switch":"1","new_backoffice_permissions_sync_switch":"1","platebuster_item_images":"1","platebuster_dealer":"1","publish_constraint_motivations":"1","tariff_service_create":0,"pricingInfmDictsAK":"1","service_price_estimator_2_phones":null,"notification_settings_banner":null,"web_push_subscribe_banner":"20","about_company_redesign_user_percentage":"100","cvPaidEnabled":"","cv_simple":"0","cv_simple_mav":"0","cv_simple_android":"0","cv_simple_ios":"0","integration_of_anonymous_number_in_the_feed_for":"0","new_subs_to_fs":"1","manager_detach_through_di":"1","package_disable_probability":"25","package_pre_finish_disable":"1","package_disable_date":"11.06.2019 12:45","mnz_infomodel_pricing_tree_version":"","apcu_mnz_navigation":"1","service_tariff_settings_get_url":"100","tariff_closing_across_data_bus":"1","service_tariff_settings_save_url":"1","tariff_cv_included":"0","subs_with_dynamic_period":"0","subscriptions_autoprolong_prohibited":"1","subscriptions_general_autoprolong_prohibited":"11.02.2020 00:00","subscriptions_services_autoprolong_prohibited":"1","tariff_migration_services":"13.11.2019 00:00","subscription_crisis_alert":"0","package_history_from_pub_history":"1","close_job_packages_date":"05.11.2019 00:00","close_general_packages_date":"05.11.2019 00:00","pfl_show_redesigned_shop_page":"113285232","increased_prices_microcategory_start":false,"increased_prices_microcategory_finish":false,"bcd_path_data_from_classificator":"100","bcd_microcat_id_tree_from_classificator":"100","mnz_extended_logging_watermark_consumer":"1","apps_tree_logging":"1","new_mav_referer_check":"1","iRNewModelProbability":"100","salesforce_test_users_subscriptions":"0","salesforce_check_opportunity_exists_in_salesforce":"1","promo_mastercard":"0","service_user_items_usage":"100","user_password_change_api_by_mapi_profile":null,"user_password_set_api_by_mapi_profile":null,"service_lf_fees_info_method":"0","service_lf_need_to_pay_source":false,"service_lf_need_to_pay_method":"0","service_lf_write_of_source":0,"service_lf_get_waiting_method":"100","service_lf_get_package_comparator":0,"delivery_marketplace_flow":"1","accounts_hierarchy_employee_link_in_header":"1","accounts_hierarchy_validate_phone":true,"accounts_hierarchy_operations_processing":"1","accounts_hierarchy_autopublish_processing":"1","accounts_hierarchy_publish_operations":"1","service_image_storage_urls_admin":null,"bad_referer_debug_bx5592_percentage":"100",'item_log_percentage":"5","mav_item_log_percentage":"5","mongo_geo_use_projection_percentage":"0","yandex_webvisor_performance_marketing_percentage":"10","iva_mapi_item_percentage":"0","fav_sellers_on_item_percentage":"100","service_search_filters":100,"show_stories_main_page":"100","ssr_header_everywhere":"0","ssr_header_item_page":"0","ssr_header_favorites_page":"0","geo_resolver_map_area":"100","geo_hash_on_apps_add_ios":"0","geo_hash_on_apps_add_android":0,"geo_hash_on_apps_add_mav":"0","infomodel_layout_check_percentage":"0","serp_facade_api_filters_enabled":false,"validation_params_use_value":"100","desktop_suggest_infm_category_by_title":"0","no_car_slot_turn_on":"1","web_snippets":100,"vasPerformance":"625670,651110,652560,626470,649330,621590,637530,629995,628455,653430,650690,640001,662280","orderContext":"1","orderContextRead":"100","orderContextWrite":"100","orderContextCompare":"100","cron_nlse_enable_extra_logging":"0","laas_frontend_shadow_requesting_percents":"100","geo_resolver_shadow_requesting_percents":"100","geo_go_service_requests_shadowing_percents":"0","geo_address_on_snippets_new":"0","geo_metro_radius_count_unlimited":"0","geo_log_fields_hash_empty_address":"0","geo_map_screenshoter_enabled":"100","geo_tyler_enabled":"100","update_contacts_filter":true,"auto_upload_problems_show_banner":"0","publish_auto_ios_use_select_instead_params":true,"seo_catalog_use_classificator_percentage":"0","seo_catalog_use_u8r_percentage":"100","seo_v2_handler_percentage_mav":"100","seo_covid_title_main":false,"sx_imv_snippet_and_card":"100","sx_through_sort":"1","admin_search_always_sphinx":"1","admin_search_phone_mask_wildcard":"1","u8r":"100","u8r_experimental":"100","u8r_mav":"100","u8r_mav_experimental":"100","u8r_mav_auto":"100","u8r_mav_search_subscriptions":"100","u8r_page_urls":"1","filters_links":"100","filters_links_auto":"100","vacancies_catalogue":"100",'item_view_delivery_item_request":"100","js_layout_shop_manager":false,"authorize_cookie_ttl":"100","require_phone_confirm_reactivation":true,"calculate_views_based_on_item_location":true,"autocatalog_add_params":"100","imv_auto_info_page":"1","big_picture_percentage":"100","avito_pro_enable_web_vizor":"1","apps_rich_snippet":"100","service_serp_display_type_enabled":"1","disable_covid_for_android_77":"1","log_rich_snippet_calltracking_latency":"1","migrate_to_redis_auth":"1","refresh_token_from_service_auth":"100","disable_jobs_produce_for_auth":"1","prfl_enable_b2c_delivery":false,"quality_badges_realty_verified":"100","social_delete_service_auth":"1","LibStatProviderViews":"1","ProStatsProviderViews":"","ProStatsProviderContacts":"1","accountant_admin_users":"1514,3523","payment_bus_users":"128083593,27392985,164917327,165508730,165668047,165738127,165795474, 165842361,165858888,165914165, 166187549,170279566","billing_data_bus_service_and_package_pairs":"[{\"serviceId\":10,\"packageId\":2},{\"serviceId\":10,\"packageId\":3},{\"serviceId\":10,\"packageId\":4},{\"serviceId\":10,\"packageId\":5},{\"serviceId\":10,\"packageId\":6},{\"serviceId\":10,\"packageId\":7},{\"serviceId\":10,\"packageId\":8},{\"serviceId\":10,\"packageId\":9},{\"serviceId\":1},{\"serviceId\":2},{\"serviceId\":3},{\"serviceId\":4},{\"serviceId\":15},{\"serviceId\":16}]","billing_data_bus_single_lf_purchase_probability":"0","billing_ttl_additional_time":0,"billingTtlEnabled":"1","billing_data_bus_order_item_ids_to_skip":"","billing_consumer_retry_forever_enabled":true,"billing_cpa_report_enabled":"1","billing_performance_vas_via_scheduler":"1","billing_fail_payment_if_sum_changed_for_apple_pay":"1","billing_show_in_progress_without_success_payment":"1","prolongationVasFromService":""}} || {};
# 3</script>
