CREATE DATABASE works_dw;

DROP TABLE IF EXISTS adventure_works_dw_build_version;
DROP TABLE IF EXISTS dim_account;
DROP TABLE IF EXISTS dim_currency;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_department_group;
DROP TABLE IF EXISTS dim_employee;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_organization;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_product_category;
DROP TABLE IF EXISTS dim_product_subcategory;
DROP TABLE IF EXISTS dim_promotion;
DROP TABLE IF EXISTS dim_reseller;
DROP TABLE IF EXISTS dim_sales_reason;
DROP TABLE IF EXISTS dim_sales_territory;
DROP TABLE IF EXISTS dim_scenario;
DROP TABLE IF EXISTS fact_additional_international_product_description;
DROP TABLE IF EXISTS fact_call_center;
DROP TABLE IF EXISTS fact_currency_rate;
DROP TABLE IF EXISTS fact_finance;
DROP TABLE IF EXISTS fact_internet_sales;
DROP TABLE IF EXISTS fact_internet_sales_reason;
DROP TABLE IF EXISTS fact_product_inventory;
DROP TABLE IF EXISTS fact_reseller_sales;
DROP TABLE IF EXISTS fact_sales_quota;
DROP TABLE IF EXISTS fact_survey_response;
DROP TABLE IF EXISTS new_fact_currency_rate;
DROP TABLE IF EXISTS prospective_buyer;


CREATE TABLE adventure_works_dw_build_version(
	db_version varchar(50) NULL,
	version_date timestamp NULL
);

CREATE TABLE dim_account(
	account_key serial NOT NULL,
	parent_account_key int NULL,
	account_code_alternate_key int NULL,
	parent_account_code_alternate_key int NULL,
	account_description varchar(50) NULL,
	account_type varchar(50) NULL,
	operator varchar(50) NULL,
	custom_members varchar(300) NULL,
	value_type varchar(50) NULL,
	custom_member_options varchar(200) NULL 
);

CREATE TABLE dim_currency(
	currency_key serial NOT NULL,
	currency_alternate_key char(3) NOT NULL,
	currency_name varchar(50) NOT NULL
);

CREATE TABLE dim_customer(
	customer_key serial NOT NULL,
	geography_key int NULL,
	customer_alternate_key varchar(15) NOT NULL,
	title varchar(8) NULL,
	first_name varchar(50) NULL,
	middle_name varchar(50) NULL,
	last_name varchar(50) NULL,
	name_style boolean NULL,
	birth_date date NULL,
	marital_status char(1) NULL,
	suffix varchar(10) NULL,
	gender varchar(1) NULL,
	email_address varchar(50) NULL,
	yearly_income numeric(19,4) NULL,
	total_children int NULL,
	number_children_at_home int NULL,
	english_education varchar(40) NULL,
	spanish_education varchar(40) NULL,
	french_education varchar(40) NULL,
	english_occupation varchar(100) NULL,
	spanish_occupation varchar(100) NULL,
	french_occupation varchar(100) NULL,
	house_owner_flag char(1) NULL,
	number_cars_owned int NULL,
	address_line1 varchar(120) NULL,
	address_line2 varchar(120) NULL,
	phone varchar(20) NULL,
	date_first_purchase date NULL,
	commute_distance varchar(15) NULL
);

CREATE TABLE dim_date(
	date_key int NOT NULL,
	full_date_alternate_key date NOT NULL,
	day_number_of_week int NOT NULL,
	english_day_name_of_week varchar(10) NOT NULL,
	spanish_day_name_of_week varchar(10) NOT NULL,
	french_day_name_of_week varchar(10) NOT NULL,
	day_number_of_month int NOT NULL,
	day_number_of_year smallint NOT NULL,
	week_number_of_year int NOT NULL,
	english_month_name varchar(10) NOT NULL,
	spanish_month_name varchar(10) NOT NULL,
	french_month_name varchar(10) NOT NULL,
	month_number_of_year int NOT NULL,
	calendar_quarter int NOT NULL,
	calendar_year smallint NOT NULL,
	calendar_semester int NOT NULL,
	fiscal_quarter int NOT NULL,
	fiscal_year smallint NOT NULL,
	fiscal_semester int NOT NULL
);

CREATE TABLE dim_department_group(
	department_group_key serial NOT NULL,
	parent_department_group_key int NULL,
	department_group_name varchar(50) NULL
);

CREATE TABLE dim_employee(
	employee_key serial NOT NULL,
	parent_employee_key int NULL,
	employee_national_id_alternate_key varchar(15) NULL,
	parent_employee_national_id_alternate_key varchar(15) NULL,
	sales_territory_key int NULL,
	first_name varchar(50) NOT NULL,
	last_name varchar(50) NOT NULL,
	middle_name varchar(50) NULL,
	name_style boolean NOT NULL,
	title varchar(50) NULL,
	hire_date date NULL,
	birth_date date NULL,
	login_id varchar(256) NULL,
	email_address varchar(50) NULL,
	phone varchar(25) NULL,
	marital_status char(1) NULL,
	emergency_contact_name varchar(50) NULL,
	emergency_contact_phone varchar(25) NULL,
	salaried_flag boolean NULL,
	gender char(1) NULL,
	pay_frequency int NULL,
	base_rate numeric(19,4) NULL,
	vacation_hours smallint NULL,
	sick_leave_hours smallint NULL,
	current_flag boolean NOT NULL,
	sales_person_flag boolean NOT NULL,
	department_name varchar(50) NULL,
	start_date date NULL,
	end_date date NULL,
	status varchar(50) NULL,
	employee_photo bytea NULL
);

CREATE TABLE dim_geography(
	geography_key serial NOT NULL,
	city varchar(30) NULL,
	state_province_code varchar(3) NULL,
	state_province_name varchar(50) NULL,
	country_region_code varchar(3) NULL,
	english_country_region_name varchar(50) NULL,
	spanish_country_region_name varchar(50) NULL,
	french_country_region_name varchar(50) NULL,
	postal_code varchar(15) NULL,
	sales_territory_key int NULL,
	ip_address_locator varchar(15) NULL
);

CREATE TABLE dim_organization(
	organization_key serial NOT NULL,
	parent_organization_key int NULL,
	percentage_of_ownership varchar(16) NULL,
	organization_name varchar(50) NULL,
	currency_key int NULL
);

CREATE TABLE dim_product(
	product_key serial NOT NULL,
	product_alternate_key varchar(25) NULL,
	product_subcategory_key int NULL,
	weight_unit_measure_code char(3) NULL,
	size_unit_measure_code char(3) NULL,
	english_product_name varchar(50) NOT NULL,
	spanish_product_name varchar(50) NOT NULL,
	french_product_name varchar(50) NOT NULL,
	standard_cost numeric(19,4) NULL,
	finished_goods_flag boolean NOT NULL,
	color varchar(15) NOT NULL,
	safety_stock_level smallint NULL,
	reorder_point smallint NULL,
	list_price numeric(19,4) NULL,
	size varchar(50) NULL,
	size_range varchar(50) NULL,
	weight double precision NULL,
	days_to_manufacture int NULL,
	product_line char(2) NULL,
	dealer_price numeric(19,4) NULL,
	class char(2) NULL,
	style char(2) NULL,
	model_name varchar(50) NULL,
	large_photo bytea NULL,
	english_description varchar(400) NULL,
	french_description varchar(400) NULL,
	chinese_description varchar(400) NULL,
	arabic_description varchar(400) NULL,
	hebrew_description varchar(400) NULL,
	thai_description varchar(400) NULL,
	german_description varchar(400) NULL,
	japanese_description varchar(400) NULL,
	turkish_description varchar(400) NULL,
	start_date timestamp NULL,
	end_date timestamp NULL,
	status varchar(7) NULL
);

CREATE TABLE dim_product_category(
	product_category_key serial NOT NULL,
	product_category_alternate_key int NULL,
	english_product_category_name varchar(50) NOT NULL,
	spanish_product_category_name varchar(50) NOT NULL,
	french_product_category_name varchar(50) NOT NULL
);

CREATE TABLE dim_product_subcategory(
	product_subcategory_key serial NOT NULL,
	product_subcategory_alternate_key int NULL,
	english_product_subcategory_name varchar(50) NOT NULL,
	spanish_product_subcategory_name varchar(50) NOT NULL,
	french_product_subcategory_name varchar(50) NOT NULL,
	product_category_key int NULL
);

CREATE TABLE dim_promotion(
	promotion_key serial NOT NULL,
	promotion_alternate_key int NULL,
	english_promotion_name varchar(255) NULL,
	spanish_promotion_name varchar(255) NULL,
	french_promotion_name varchar(255) NULL,
	discount_pct double precision NULL,
	english_promotion_type varchar(50) NULL,
	spanish_promotion_type varchar(50) NULL,
	french_promotion_type varchar(50) NULL,
	english_promotion_category varchar(50) NULL,
	spanish_promotion_category varchar(50) NULL,
	french_promotion_category varchar(50) NULL,
	start_date timestamp NOT NULL,
	end_date timestamp NULL,
	min_qty int NULL,
	max_qty int NULL
);

CREATE TABLE dim_reseller(
	reseller_key serial NOT NULL,
	geography_key int NULL,
	reseller_alternate_key varchar(15) NULL,
	phone varchar(25) NULL,
	business_type varchar(20) NOT NULL,
	reseller_name varchar(50) NOT NULL,
	number_employees int NULL,
	order_frequency char(1) NULL,
	order_month int NULL,
	first_order_year int NULL,
	last_order_year int NULL,
	product_line varchar(50) NULL,
	address_line1 varchar(60) NULL,
	address_line2 varchar(60) NULL,
	annual_sales numeric(19,4) NULL,
	bank_name varchar(50) NULL,
	min_payment_type int NULL,
	min_payment_amount numeric(19,4) NULL,
	annual_revenue numeric(19,4) NULL,
	year_opened int NULL
);

CREATE TABLE dim_sales_reason(
	sales_reason_key serial NOT NULL,
	sales_reason_alternate_key int NOT NULL,
	sales_reason_name varchar(50) NOT NULL,
	sales_reason_reason_type varchar(50) NOT NULL
);

CREATE TABLE dim_sales_territory(
	sales_territory_key serial NOT NULL,
	sales_territory_alternate_key int NULL,
	sales_territory_region varchar(50) NOT NULL,
	sales_territory_country varchar(50) NOT NULL,
	sales_territory_group varchar(50) NULL,
	sales_territory_image bytea NULL
);

CREATE TABLE dim_scenario(
	scenario_key serial NOT NULL,
	scenario_name varchar(50) NULL
);

CREATE TABLE fact_additional_international_product_description(
	product_key int NOT NULL,
	culture_name varchar(50) NOT NULL,
	product_description varchar(512) NOT NULL
);

CREATE TABLE fact_call_center(
	fact_call_center_id serial NOT NULL,
	date_key int NOT NULL,
	wage_type varchar(15) NOT NULL,
	shift varchar(20) NOT NULL,
	level_one_operators smallint NOT NULL,
	level_two_operators smallint NOT NULL,
	total_operators smallint NOT NULL,
	calls int NOT NULL,
	automatic_responses int NOT NULL,
	orders int NOT NULL,
	issues_raised smallint NOT NULL,
	average_time_per_issue smallint NOT NULL,
	service_grade double precision NOT NULL,
	date timestamp NULL
);

CREATE TABLE fact_currency_rate(
	currency_key int NOT NULL,
	date_key int NOT NULL,
	average_rate double precision NOT NULL,
	end_of_day_rate double precision NOT NULL,
	date timestamp NULL
);

CREATE TABLE fact_finance(
	finance_key serial NOT NULL,
	date_key int NOT NULL,
	organization_key int NOT NULL,
	department_group_key int NOT NULL,
	scenario_key int NOT NULL,
	account_key int NOT NULL,
	amount double precision NOT NULL,
	date timestamp NULL
);

CREATE TABLE fact_internet_sales(
	product_key int NOT NULL,
	order_date_key int NOT NULL,
	due_date_key int NOT NULL,
	ship_date_key int NOT NULL,
	customer_key int NOT NULL,
	promotion_key int NOT NULL,
	currency_key int NOT NULL,
	sales_territory_key int NOT NULL,
	sales_order_number varchar(20) NOT NULL,
	sales_order_line_number int NOT NULL,
	revision_number int NOT NULL,
	order_quantity smallint NOT NULL,
	unit_price numeric(19,4) NOT NULL,
	extended_amount numeric(19,4) NOT NULL,
	unit_price_discount_pct double precision NOT NULL,
	discount_amount double precision NOT NULL,
	product_standard_cost numeric(19,4) NOT NULL,
	total_product_cost numeric(19,4) NOT NULL,
	sales_amount numeric(19,4) NOT NULL,
	tax_amt numeric(19,4) NOT NULL,
	freight numeric(19,4) NOT NULL,
	carrier_tracking_number varchar(25) NULL,
	customer_po_number varchar(25) NULL,
	order_date timestamp NULL,
	due_date timestamp NULL,
	ship_date timestamp NULL
);

CREATE TABLE fact_internet_sales_reason(
	sales_order_number varchar(20) NOT NULL,
	sales_order_line_number int NOT NULL,
	sales_reason_key int NOT NULL
);

CREATE TABLE fact_product_inventory(
	product_key int NOT NULL,
	date_key int NOT NULL,
	movement_date date NOT NULL,
	unit_cost numeric(19,4) NOT NULL,
	units_in int NOT NULL,
	units_out int NOT NULL,
	units_balance int NOT NULL
);

CREATE TABLE fact_reseller_sales(
	product_key int NOT NULL,
	order_date_key int NOT NULL,
	due_date_key int NOT NULL,
	ship_date_key int NOT NULL,
	reseller_key int NOT NULL,
	employee_key int NOT NULL,
	promotion_key int NOT NULL,
	currency_key int NOT NULL,
	sales_territory_key int NOT NULL,
	sales_order_number varchar(20) NOT NULL,
	sales_order_line_number int NOT NULL,
	revision_number int NULL,
	order_quantity smallint NULL,
	unit_price numeric(19,4) NULL,
	extended_amount numeric(19,4) NULL,
	unit_price_discount_pct double precision NULL,
	discount_amount double precision NULL,
	product_standard_cost numeric(19,4) NULL,
	total_product_cost numeric(19,4) NULL,
	sales_amount numeric(19,4) NULL,
	tax_amt numeric(19,4) NULL,
	freight numeric(19,4) NULL,
	carrier_tracking_number varchar(25) NULL,
	customer_po_number varchar(25) NULL,
	order_date timestamp NULL,
	due_date timestamp NULL,
	ship_date timestamp NULL
);

CREATE TABLE fact_sales_quota(
	sales_quota_key serial NOT NULL,
	employee_key int NOT NULL,
	date_key int NOT NULL,
	calendar_year smallint NOT NULL,
	calendar_quarter int NOT NULL,
	sales_amount_quota numeric(19,4) NOT NULL,
	date timestamp NULL
);

CREATE TABLE fact_survey_response(
	survey_response_key serial NOT NULL,
	date_key int NOT NULL,
	customer_key int NOT NULL,
	product_category_key int NOT NULL,
	english_product_category_name varchar(50) NOT NULL,
	product_subcategory_key int NOT NULL,
	english_product_subcategory_name varchar(50) NOT NULL,
	date timestamp NULL
);

CREATE TABLE new_fact_currency_rate(
	average_rate real NULL,
	currency_id varchar(3) NULL,
	currency_date date NULL,
	end_of_day_rate real NULL,
	currency_key int NULL,
	date_key int NULL
);

CREATE TABLE prospective_buyer(
	prospective_buyer_key serial NOT NULL,
	prospect_alternate_key varchar(15) NULL,
	first_name varchar(50) NULL,
	middle_name varchar(50) NULL,
	last_name varchar(50) NULL,
	birth_date timestamp NULL,
	marital_status char(1) NULL,
	gender varchar(1) NULL,
	email_address varchar(50) NULL,
	yearly_income numeric(19,4) NULL,
	total_children int NULL,
	number_children_at_home int NULL,
	education varchar(40) NULL,
	occupation varchar(100) NULL,
	house_owner_flag char(1) NULL,
	number_cars_owned int NULL,
	address_line1 varchar(120) NULL,
	address_line2 varchar(120) NULL,
	city varchar(30) NULL,
	state_province_code varchar(3) NULL,
	postal_code varchar(15) NULL,
	phone varchar(20) NULL,
	salutation varchar(8) NULL,
	unknown int NULL
);

ALTER TABLE dim_account ADD CONSTRAINT fk_dimaccount_dimaccount FOREIGN KEY (parent_account_key) REFERENCES dim_account (account_key);
ALTER TABLE dim_customer ADD CONSTRAINT fk_dimcustomer_dimgeography FOREIGN KEY (geography_key) REFERENCES dim_geography (geography_key);
ALTER TABLE dim_department_group ADD CONSTRAINT fk_dimdepartmentgroup_dimdepartmentgroup FOREIGN KEY (parent_department_group_key) REFERENCES dim_department_group (department_group_key);
ALTER TABLE dim_employee ADD CONSTRAINT fk_dimemployee_dimsalesterritory FOREIGN KEY (sales_territory_key) REFERENCES dim_sales_territory (sales_territory_key);
ALTER TABLE dim_geography ADD CONSTRAINT fk_dimgeography_dimsalesterritory FOREIGN KEY (sales_territory_key) REFERENCES dim_sales_territory (sales_territory_key);
ALTER TABLE dim_organization ADD CONSTRAINT fk_dimorganization_dimcurrency FOREIGN KEY (currency_key) REFERENCES dim_currency (currency_key);
ALTER TABLE dim_product ADD CONSTRAINT fk_dimproduct_dimproductsubcategory FOREIGN KEY (product_subcategory_key) REFERENCES dim_product_subcategory (product_subcategory_key);
ALTER TABLE dim_product_subcategory ADD CONSTRAINT fk_dimproductsubcategory_dimproductcategory FOREIGN KEY (product_category_key) REFERENCES dim_product_category (product_category_key);
ALTER TABLE dim_reseller ADD CONSTRAINT fk_dimreseller_dimgeography FOREIGN KEY (geography_key) REFERENCES dim_geography (geography_key);
ALTER TABLE fact_call_center ADD CONSTRAINT fk_factcallcenter_dimdate FOREIGN KEY (date_key) REFERENCES dim_date (date_key);
ALTER TABLE fact_currency_rate ADD CONSTRAINT fk_factcurrencyrate_dimdate FOREIGN KEY (date_key) REFERENCES dim_date (date_key);
ALTER TABLE fact_finance ADD CONSTRAINT fk_factfinance_dimscenario FOREIGN KEY (scenario_key) REFERENCES dim_scenario (scenario_key);
ALTER TABLE fact_internet_sales ADD CONSTRAINT fk_factinternetsales_dimcurrency FOREIGN KEY (currency_key) REFERENCES dim_currency (currency_key);
ALTER TABLE fact_reseller_sales ADD CONSTRAINT fk_factresellersales_dimcurrency FOREIGN KEY (currency_key) REFERENCES dim_currency (currency_key);
ALTER TABLE fact_sales_quota ADD CONSTRAINT fk_factsalesquota_dimemployee FOREIGN KEY (employee_key) REFERENCES dim_employee (employee_key);
ALTER TABLE fact_survey_response ADD CONSTRAINT fk_factsurveyresponse_datekey FOREIGN KEY (date_key) REFERENCES dim_date (date_key);

COMMENT ON TABLE adventure_works_dw_build_version IS '数据仓库版本信息';
COMMENT ON TABLE dim_account IS '账户维表';
COMMENT ON TABLE dim_currency IS '货币维表';
COMMENT ON TABLE dim_customer IS '客户维表';
COMMENT ON TABLE dim_date IS '日期维表';
COMMENT ON TABLE dim_department_group IS '部门组维表';
COMMENT ON TABLE dim_employee IS '员工维表';
COMMENT ON TABLE dim_geography IS '地理区域维表';
COMMENT ON TABLE dim_organization IS '组织结构维表';
COMMENT ON TABLE dim_product IS '产品维表';
COMMENT ON TABLE dim_product_category IS '产品大类维表';
COMMENT ON TABLE dim_product_subcategory IS '产品子类维表';
COMMENT ON TABLE dim_promotion IS '促销维表';
COMMENT ON TABLE dim_reseller IS '分销商维表';
COMMENT ON TABLE dim_sales_reason IS '销售原因维表';
COMMENT ON TABLE dim_sales_territory IS '销售区域维表';
COMMENT ON TABLE dim_scenario IS '业务场景维表';
COMMENT ON TABLE fact_additional_international_product_description IS '国际产品扩展描述事实表';
COMMENT ON TABLE fact_call_center IS '呼叫中心事实表';
COMMENT ON TABLE fact_currency_rate IS '货币汇率事实表';
COMMENT ON TABLE fact_finance IS '财务事实表';
COMMENT ON TABLE fact_internet_sales IS '互联网销售事实表';
COMMENT ON TABLE fact_internet_sales_reason IS '互联网销售原因事实表';
COMMENT ON TABLE fact_product_inventory IS '产品库存事实表';
COMMENT ON TABLE fact_reseller_sales IS '分销商销售事实表';
COMMENT ON TABLE fact_sales_quota IS '销售配额事实表';
COMMENT ON TABLE fact_survey_response IS '问卷调查响应事实表';
COMMENT ON TABLE new_fact_currency_rate IS '新货币汇率事实表';
COMMENT ON TABLE prospective_buyer IS '潜在客户事实表';
COMMENT ON TABLE sysdiagrams IS '系统图表';
COMMENT ON COLUMN adventure_works_dw_build_version.db_version IS 'db版本';
COMMENT ON COLUMN adventure_works_dw_build_version.version_date IS '版本日期';
COMMENT ON COLUMN dim_account.account_key IS '账户主键/外键标识';
COMMENT ON COLUMN dim_account.parent_account_key IS 'parent账户主键/外键标识';
COMMENT ON COLUMN dim_account.account_code_alternate_key IS '账户代码备用主键/外键标识';
COMMENT ON COLUMN dim_account.parent_account_code_alternate_key IS 'parent账户代码备用主键/外键标识';
COMMENT ON COLUMN dim_account.account_description IS '账户描述';
COMMENT ON COLUMN dim_account.account_type IS '账户类型';
COMMENT ON COLUMN dim_account.operator IS 'operator';
COMMENT ON COLUMN dim_account.custom_members IS 'custommembers';
COMMENT ON COLUMN dim_account.value_type IS 'value类型';
COMMENT ON COLUMN dim_account.custom_member_options IS 'custommemberoptions';
COMMENT ON COLUMN dim_currency.currency_key IS '货币主键';
COMMENT ON COLUMN dim_currency.currency_alternate_key IS '货币备用主键/外键标识';
COMMENT ON COLUMN dim_currency.currency_name IS '货币名称';
COMMENT ON COLUMN dim_customer.customer_key IS '客户主键';
COMMENT ON COLUMN dim_customer.geography_key IS 'geography主键/外键标识';
COMMENT ON COLUMN dim_customer.customer_alternate_key IS '客户备用主键/外键标识';
COMMENT ON COLUMN dim_customer.title IS 'title';
COMMENT ON COLUMN dim_customer.first_name IS '第一次名称';
COMMENT ON COLUMN dim_customer.middle_name IS 'middle名称';
COMMENT ON COLUMN dim_customer.last_name IS '最后一次名称';
COMMENT ON COLUMN dim_customer.name_style IS '名称style';
COMMENT ON COLUMN dim_customer.birth_date IS '出生日期';
COMMENT ON COLUMN dim_customer.marital_status IS '婚姻状态';
COMMENT ON COLUMN dim_customer.suffix IS 'suffix';
COMMENT ON COLUMN dim_customer.gender IS '性别';
COMMENT ON COLUMN dim_customer.email_address IS '电子邮箱';
COMMENT ON COLUMN dim_customer.yearly_income IS 'yearly收入';
COMMENT ON COLUMN dim_customer.total_children IS '总计children';
COMMENT ON COLUMN dim_customer.number_children_at_home IS '编号childrenathome';
COMMENT ON COLUMN dim_customer.english_education IS 'english教育';
COMMENT ON COLUMN dim_customer.spanish_education IS 'spanish教育';
COMMENT ON COLUMN dim_customer.french_education IS 'french教育';
COMMENT ON COLUMN dim_customer.english_occupation IS 'englishoccupation';
COMMENT ON COLUMN dim_customer.spanish_occupation IS 'spanishoccupation';
COMMENT ON COLUMN dim_customer.french_occupation IS 'frenchoccupation';
COMMENT ON COLUMN dim_customer.house_owner_flag IS 'houseowner标记';
COMMENT ON COLUMN dim_customer.number_cars_owned IS '编号carsowned';
COMMENT ON COLUMN dim_customer.phone IS '电话';
COMMENT ON COLUMN dim_customer.date_first_purchase IS '日期第一次purchase';
COMMENT ON COLUMN dim_customer.commute_distance IS 'commutedistance';
COMMENT ON COLUMN dim_date.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN dim_date.full_date_alternate_key IS 'full日期备用主键/外键标识';
COMMENT ON COLUMN dim_date.day_number_of_week IS '天编号ofweek';
COMMENT ON COLUMN dim_date.english_day_name_of_week IS 'english天名称ofweek';
COMMENT ON COLUMN dim_date.spanish_day_name_of_week IS 'spanish天名称ofweek';
COMMENT ON COLUMN dim_date.french_day_name_of_week IS 'french天名称ofweek';
COMMENT ON COLUMN dim_date.day_number_of_month IS '天编号of月份';
COMMENT ON COLUMN dim_date.day_number_of_year IS '天编号of年份';
COMMENT ON COLUMN dim_date.week_number_of_year IS 'week编号of年份';
COMMENT ON COLUMN dim_date.english_month_name IS 'english月份名称';
COMMENT ON COLUMN dim_date.spanish_month_name IS 'spanish月份名称';
COMMENT ON COLUMN dim_date.french_month_name IS 'french月份名称';
COMMENT ON COLUMN dim_date.month_number_of_year IS '月份编号of年份';
COMMENT ON COLUMN dim_date.calendar_quarter IS 'calendarquarter';
COMMENT ON COLUMN dim_date.calendar_year IS 'calendar年份';
COMMENT ON COLUMN dim_date.calendar_semester IS 'calendarsemester';
COMMENT ON COLUMN dim_date.fiscal_quarter IS 'fiscalquarter';
COMMENT ON COLUMN dim_date.fiscal_year IS 'fiscal年份';
COMMENT ON COLUMN dim_date.fiscal_semester IS 'fiscalsemester';
COMMENT ON COLUMN dim_department_group.department_group_key IS '部门group主键/外键标识';
COMMENT ON COLUMN dim_department_group.parent_department_group_key IS 'parent部门group主键/外键标识';
COMMENT ON COLUMN dim_department_group.department_group_name IS '部门group名称';
COMMENT ON COLUMN dim_employee.employee_key IS '员工主键';
COMMENT ON COLUMN dim_employee.parent_employee_key IS 'parent员工主键/外键标识';
COMMENT ON COLUMN dim_employee.employee_national_id_alternate_key IS '员工nationalid备用主键/外键标识';
COMMENT ON COLUMN dim_employee.parent_employee_national_id_alternate_key IS 'parent员工nationalid备用主键/外键标识';
COMMENT ON COLUMN dim_employee.sales_territory_key IS '销售区域主键';
COMMENT ON COLUMN dim_employee.first_name IS '第一次名称';
COMMENT ON COLUMN dim_employee.last_name IS '最后一次名称';
COMMENT ON COLUMN dim_employee.middle_name IS 'middle名称';
COMMENT ON COLUMN dim_employee.name_style IS '名称style';
COMMENT ON COLUMN dim_employee.title IS 'title';
COMMENT ON COLUMN dim_employee.hire_date IS 'hire日期';
COMMENT ON COLUMN dim_employee.birth_date IS '出生日期';
COMMENT ON COLUMN dim_employee.login_id IS 'loginid';
COMMENT ON COLUMN dim_employee.email_address IS '电子邮箱';
COMMENT ON COLUMN dim_employee.phone IS '电话';
COMMENT ON COLUMN dim_employee.marital_status IS '婚姻状态';
COMMENT ON COLUMN dim_employee.emergency_contact_name IS 'emergencycontact名称';
COMMENT ON COLUMN dim_employee.emergency_contact_phone IS 'emergencycontact电话';
COMMENT ON COLUMN dim_employee.salaried_flag IS 'salaried标记';
COMMENT ON COLUMN dim_employee.gender IS '性别';
COMMENT ON COLUMN dim_employee.pay_frequency IS 'payfrequency';
COMMENT ON COLUMN dim_employee.base_rate IS 'base比率';
COMMENT ON COLUMN dim_employee.vacation_hours IS 'vacationhours';
COMMENT ON COLUMN dim_employee.sick_leave_hours IS 'sickleavehours';
COMMENT ON COLUMN dim_employee.current_flag IS 'current标记';
COMMENT ON COLUMN dim_employee.sales_person_flag IS '销售person标记';
COMMENT ON COLUMN dim_employee.department_name IS '部门名称';
COMMENT ON COLUMN dim_employee.start_date IS 'start日期';
COMMENT ON COLUMN dim_employee.end_date IS 'end日期';
COMMENT ON COLUMN dim_employee.status IS '状态';
COMMENT ON COLUMN dim_employee.employee_photo IS '员工photo';
COMMENT ON COLUMN dim_geography.geography_key IS 'geography主键/外键标识';
COMMENT ON COLUMN dim_geography.city IS 'city';
COMMENT ON COLUMN dim_geography.state_province_code IS 'stateprovince代码';
COMMENT ON COLUMN dim_geography.state_province_name IS 'stateprovince名称';
COMMENT ON COLUMN dim_geography.country_region_code IS 'country地区代码';
COMMENT ON COLUMN dim_geography.english_country_region_name IS 'englishcountry地区名称';
COMMENT ON COLUMN dim_geography.spanish_country_region_name IS 'spanishcountry地区名称';
COMMENT ON COLUMN dim_geography.french_country_region_name IS 'frenchcountry地区名称';
COMMENT ON COLUMN dim_geography.postal_code IS '邮政编码';
COMMENT ON COLUMN dim_geography.sales_territory_key IS '销售区域主键';
COMMENT ON COLUMN dim_geography.ip_address_locator IS 'ip地址locator';
COMMENT ON COLUMN dim_organization.organization_key IS '组织主键/外键标识';
COMMENT ON COLUMN dim_organization.parent_organization_key IS 'parent组织主键/外键标识';
COMMENT ON COLUMN dim_organization.percentage_of_ownership IS 'percentageofownership';
COMMENT ON COLUMN dim_organization.organization_name IS '组织名称';
COMMENT ON COLUMN dim_organization.currency_key IS '货币主键';
COMMENT ON COLUMN dim_product.product_key IS '产品主键';
COMMENT ON COLUMN dim_product.product_alternate_key IS '产品备用主键/外键标识';
COMMENT ON COLUMN dim_product.product_subcategory_key IS '产品子类主键';
COMMENT ON COLUMN dim_product.weight_unit_measure_code IS '重量unitmeasure代码';
COMMENT ON COLUMN dim_product.size_unit_measure_code IS 'sizeunitmeasure代码';
COMMENT ON COLUMN dim_product.english_product_name IS 'english产品名称';
COMMENT ON COLUMN dim_product.spanish_product_name IS 'spanish产品名称';
COMMENT ON COLUMN dim_product.french_product_name IS 'french产品名称';
COMMENT ON COLUMN dim_product.standard_cost IS '标准成本';
COMMENT ON COLUMN dim_product.finished_goods_flag IS 'finishedgoods标记';
COMMENT ON COLUMN dim_product.color IS '颜色';
COMMENT ON COLUMN dim_product.safety_stock_level IS 'safetystocklevel';
COMMENT ON COLUMN dim_product.reorder_point IS 'reorderpoint';
COMMENT ON COLUMN dim_product.list_price IS 'list价格';
COMMENT ON COLUMN dim_product.size IS 'size';
COMMENT ON COLUMN dim_product.size_range IS 'sizerange';
COMMENT ON COLUMN dim_product.weight IS '重量';
COMMENT ON COLUMN dim_product.days_to_manufacture IS 'daystomanufacture';
COMMENT ON COLUMN dim_product.product_line IS '产品线';
COMMENT ON COLUMN dim_product.dealer_price IS 'dealer价格';
COMMENT ON COLUMN dim_product.class IS 'class';
COMMENT ON COLUMN dim_product.style IS 'style';
COMMENT ON COLUMN dim_product.model_name IS 'model名称';
COMMENT ON COLUMN dim_product.large_photo IS 'largephoto';
COMMENT ON COLUMN dim_product.english_description IS 'english描述';
COMMENT ON COLUMN dim_product.french_description IS 'french描述';
COMMENT ON COLUMN dim_product.chinese_description IS 'chinese描述';
COMMENT ON COLUMN dim_product.arabic_description IS 'arabic描述';
COMMENT ON COLUMN dim_product.hebrew_description IS 'hebrew描述';
COMMENT ON COLUMN dim_product.thai_description IS 'thai描述';
COMMENT ON COLUMN dim_product.german_description IS 'german描述';
COMMENT ON COLUMN dim_product.japanese_description IS 'japanese描述';
COMMENT ON COLUMN dim_product.turkish_description IS 'turkish描述';
COMMENT ON COLUMN dim_product.start_date IS 'start日期';
COMMENT ON COLUMN dim_product.end_date IS 'end日期';
COMMENT ON COLUMN dim_product.status IS '状态';
COMMENT ON COLUMN dim_product_category.product_category_key IS '产品大类主键';
COMMENT ON COLUMN dim_product_category.product_category_alternate_key IS '产品category备用主键/外键标识';
COMMENT ON COLUMN dim_product_category.english_product_category_name IS 'english产品category名称';
COMMENT ON COLUMN dim_product_category.spanish_product_category_name IS 'spanish产品category名称';
COMMENT ON COLUMN dim_product_category.french_product_category_name IS 'french产品category名称';
COMMENT ON COLUMN dim_product_subcategory.product_subcategory_key IS '产品子类主键';
COMMENT ON COLUMN dim_product_subcategory.product_subcategory_alternate_key IS '产品subcategory备用主键/外键标识';
COMMENT ON COLUMN dim_product_subcategory.english_product_subcategory_name IS 'english产品subcategory名称';
COMMENT ON COLUMN dim_product_subcategory.spanish_product_subcategory_name IS 'spanish产品subcategory名称';
COMMENT ON COLUMN dim_product_subcategory.french_product_subcategory_name IS 'french产品subcategory名称';
COMMENT ON COLUMN dim_product_subcategory.product_category_key IS '产品大类主键';
COMMENT ON COLUMN dim_promotion.promotion_key IS '促销主键';
COMMENT ON COLUMN dim_promotion.promotion_alternate_key IS '促销备用主键/外键标识';
COMMENT ON COLUMN dim_promotion.english_promotion_name IS 'english促销名称';
COMMENT ON COLUMN dim_promotion.spanish_promotion_name IS 'spanish促销名称';
COMMENT ON COLUMN dim_promotion.french_promotion_name IS 'french促销名称';
COMMENT ON COLUMN dim_promotion.discount_pct IS '折扣百分比';
COMMENT ON COLUMN dim_promotion.english_promotion_type IS 'english促销类型';
COMMENT ON COLUMN dim_promotion.spanish_promotion_type IS 'spanish促销类型';
COMMENT ON COLUMN dim_promotion.french_promotion_type IS 'french促销类型';
COMMENT ON COLUMN dim_promotion.english_promotion_category IS 'english促销category';
COMMENT ON COLUMN dim_promotion.spanish_promotion_category IS 'spanish促销category';
COMMENT ON COLUMN dim_promotion.french_promotion_category IS 'french促销category';
COMMENT ON COLUMN dim_promotion.start_date IS 'start日期';
COMMENT ON COLUMN dim_promotion.end_date IS 'end日期';
COMMENT ON COLUMN dim_promotion.min_qty IS 'minqty';
COMMENT ON COLUMN dim_promotion.max_qty IS 'maxqty';
COMMENT ON COLUMN dim_reseller.reseller_key IS '分销商主键';
COMMENT ON COLUMN dim_reseller.geography_key IS 'geography主键/外键标识';
COMMENT ON COLUMN dim_reseller.reseller_alternate_key IS 'reseller备用主键/外键标识';
COMMENT ON COLUMN dim_reseller.phone IS '电话';
COMMENT ON COLUMN dim_reseller.business_type IS 'business类型';
COMMENT ON COLUMN dim_reseller.reseller_name IS 'reseller名称';
COMMENT ON COLUMN dim_reseller.number_employees IS '编号employees';
COMMENT ON COLUMN dim_reseller.order_frequency IS '订单frequency';
COMMENT ON COLUMN dim_reseller.order_month IS '订单月份';
COMMENT ON COLUMN dim_reseller.first_order_year IS '首次订单年份';
COMMENT ON COLUMN dim_reseller.last_order_year IS '最后订单年份';
COMMENT ON COLUMN dim_reseller.product_line IS '产品线';
COMMENT ON COLUMN dim_reseller.annual_sales IS 'annual销售';
COMMENT ON COLUMN dim_reseller.bank_name IS 'bank名称';
COMMENT ON COLUMN dim_reseller.min_payment_type IS 'minpayment类型';
COMMENT ON COLUMN dim_reseller.min_payment_amount IS 'minpayment金额';
COMMENT ON COLUMN dim_reseller.annual_revenue IS 'annualrevenue';
COMMENT ON COLUMN dim_reseller.year_opened IS '年份opened';
COMMENT ON COLUMN dim_sales_reason.sales_reason_key IS '销售原因主键/外键标识';
COMMENT ON COLUMN dim_sales_reason.sales_reason_alternate_key IS '销售原因备用主键/外键标识';
COMMENT ON COLUMN dim_sales_reason.sales_reason_name IS '销售原因名称';
COMMENT ON COLUMN dim_sales_reason.sales_reason_reason_type IS '销售原因原因类型';
COMMENT ON COLUMN dim_sales_territory.sales_territory_key IS '销售区域主键';
COMMENT ON COLUMN dim_sales_territory.sales_territory_alternate_key IS '销售territory备用主键/外键标识';
COMMENT ON COLUMN dim_sales_territory.sales_territory_region IS '销售territory地区';
COMMENT ON COLUMN dim_sales_territory.sales_territory_country IS '销售territorycountry';
COMMENT ON COLUMN dim_sales_territory.sales_territory_group IS '销售territorygroup';
COMMENT ON COLUMN dim_sales_territory.sales_territory_image IS '销售territoryimage';
COMMENT ON COLUMN dim_scenario.scenario_key IS 'scenario主键/外键标识';
COMMENT ON COLUMN dim_scenario.scenario_name IS 'scenario名称';
COMMENT ON COLUMN fact_additional_international_product_description.product_key IS '产品主键';
COMMENT ON COLUMN fact_additional_international_product_description.culture_name IS 'culture名称';
COMMENT ON COLUMN fact_additional_international_product_description.product_description IS '产品描述';
COMMENT ON COLUMN fact_call_center.fact_call_center_id IS 'factcallcenterid';
COMMENT ON COLUMN fact_call_center.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_call_center.wage_type IS 'wage类型';
COMMENT ON COLUMN fact_call_center.shift IS 'shift';
COMMENT ON COLUMN fact_call_center.level_one_operators IS 'leveloneoperators';
COMMENT ON COLUMN fact_call_center.level_two_operators IS 'leveltwooperators';
COMMENT ON COLUMN fact_call_center.total_operators IS '总计operators';
COMMENT ON COLUMN fact_call_center.calls IS 'calls';
COMMENT ON COLUMN fact_call_center.automatic_responses IS 'automaticresponses';
COMMENT ON COLUMN fact_call_center.orders IS 'orders';
COMMENT ON COLUMN fact_call_center.issues_raised IS 'issuesraised';
COMMENT ON COLUMN fact_call_center.average_time_per_issue IS 'averagetimeperissue';
COMMENT ON COLUMN fact_call_center.service_grade IS 'servicegrade';
COMMENT ON COLUMN fact_call_center.date IS '日期';
COMMENT ON COLUMN fact_currency_rate.currency_key IS '货币主键';
COMMENT ON COLUMN fact_currency_rate.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_currency_rate.average_rate IS 'average比率';
COMMENT ON COLUMN fact_currency_rate.end_of_day_rate IS 'endof天比率';
COMMENT ON COLUMN fact_currency_rate.date IS '日期';
COMMENT ON COLUMN fact_finance.finance_key IS 'finance主键/外键标识';
COMMENT ON COLUMN fact_finance.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_finance.organization_key IS '组织主键/外键标识';
COMMENT ON COLUMN fact_finance.department_group_key IS '部门group主键/外键标识';
COMMENT ON COLUMN fact_finance.scenario_key IS 'scenario主键/外键标识';
COMMENT ON COLUMN fact_finance.account_key IS '账户主键/外键标识';
COMMENT ON COLUMN fact_finance.amount IS '金额';
COMMENT ON COLUMN fact_finance.date IS '日期';
COMMENT ON COLUMN fact_internet_sales.product_key IS '产品主键';
COMMENT ON COLUMN fact_internet_sales.order_date_key IS '下单日期主键';
COMMENT ON COLUMN fact_internet_sales.due_date_key IS '应付日期主键';
COMMENT ON COLUMN fact_internet_sales.ship_date_key IS '发货日期主键';
COMMENT ON COLUMN fact_internet_sales.customer_key IS '客户主键';
COMMENT ON COLUMN fact_internet_sales.promotion_key IS '促销主键';
COMMENT ON COLUMN fact_internet_sales.currency_key IS '货币主键';
COMMENT ON COLUMN fact_internet_sales.sales_territory_key IS '销售区域主键';
COMMENT ON COLUMN fact_internet_sales.sales_order_number IS '销售订单编号';
COMMENT ON COLUMN fact_internet_sales.sales_order_line_number IS '销售订单行编号';
COMMENT ON COLUMN fact_internet_sales.revision_number IS 'revision编号';
COMMENT ON COLUMN fact_internet_sales.order_quantity IS '订单数量';
COMMENT ON COLUMN fact_internet_sales.unit_price IS '单价';
COMMENT ON COLUMN fact_internet_sales.extended_amount IS '扩展金额';
COMMENT ON COLUMN fact_internet_sales.unit_price_discount_pct IS '单价折扣百分比';
COMMENT ON COLUMN fact_internet_sales.discount_amount IS '折扣金额';
COMMENT ON COLUMN fact_internet_sales.product_standard_cost IS '产品standard成本';
COMMENT ON COLUMN fact_internet_sales.total_product_cost IS '产品总成本';
COMMENT ON COLUMN fact_internet_sales.sales_amount IS '销售金额';
COMMENT ON COLUMN fact_internet_sales.tax_amt IS '税额';
COMMENT ON COLUMN fact_internet_sales.freight IS '运费';
COMMENT ON COLUMN fact_internet_sales.carrier_tracking_number IS 'carriertracking编号';
COMMENT ON COLUMN fact_internet_sales.customer_po_number IS '客户po编号';
COMMENT ON COLUMN fact_internet_sales.order_date IS '下单日期';
COMMENT ON COLUMN fact_internet_sales.due_date IS '应付日期';
COMMENT ON COLUMN fact_internet_sales.ship_date IS '发货日期';
COMMENT ON COLUMN fact_internet_sales_reason.sales_order_number IS '销售订单编号';
COMMENT ON COLUMN fact_internet_sales_reason.sales_order_line_number IS '销售订单行编号';
COMMENT ON COLUMN fact_internet_sales_reason.sales_reason_key IS '销售原因主键/外键标识';
COMMENT ON COLUMN fact_product_inventory.product_key IS '产品主键';
COMMENT ON COLUMN fact_product_inventory.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_product_inventory.movement_date IS 'movement日期';
COMMENT ON COLUMN fact_product_inventory.unit_cost IS 'unit成本';
COMMENT ON COLUMN fact_product_inventory.units_in IS 'unitsin';
COMMENT ON COLUMN fact_product_inventory.units_out IS 'unitsout';
COMMENT ON COLUMN fact_product_inventory.units_balance IS 'unitsbalance';
COMMENT ON COLUMN fact_reseller_sales.product_key IS '产品主键';
COMMENT ON COLUMN fact_reseller_sales.order_date_key IS '下单日期主键';
COMMENT ON COLUMN fact_reseller_sales.due_date_key IS '应付日期主键';
COMMENT ON COLUMN fact_reseller_sales.ship_date_key IS '发货日期主键';
COMMENT ON COLUMN fact_reseller_sales.reseller_key IS '分销商主键';
COMMENT ON COLUMN fact_reseller_sales.employee_key IS '员工主键';
COMMENT ON COLUMN fact_reseller_sales.promotion_key IS '促销主键';
COMMENT ON COLUMN fact_reseller_sales.currency_key IS '货币主键';
COMMENT ON COLUMN fact_reseller_sales.sales_territory_key IS '销售区域主键';
COMMENT ON COLUMN fact_reseller_sales.sales_order_number IS '销售订单编号';
COMMENT ON COLUMN fact_reseller_sales.sales_order_line_number IS '销售订单行编号';
COMMENT ON COLUMN fact_reseller_sales.revision_number IS 'revision编号';
COMMENT ON COLUMN fact_reseller_sales.order_quantity IS '订单数量';
COMMENT ON COLUMN fact_reseller_sales.unit_price IS '单价';
COMMENT ON COLUMN fact_reseller_sales.extended_amount IS '扩展金额';
COMMENT ON COLUMN fact_reseller_sales.unit_price_discount_pct IS '单价折扣百分比';
COMMENT ON COLUMN fact_reseller_sales.discount_amount IS '折扣金额';
COMMENT ON COLUMN fact_reseller_sales.product_standard_cost IS '产品standard成本';
COMMENT ON COLUMN fact_reseller_sales.total_product_cost IS '产品总成本';
COMMENT ON COLUMN fact_reseller_sales.sales_amount IS '销售金额';
COMMENT ON COLUMN fact_reseller_sales.tax_amt IS '税额';
COMMENT ON COLUMN fact_reseller_sales.freight IS '运费';
COMMENT ON COLUMN fact_reseller_sales.carrier_tracking_number IS 'carriertracking编号';
COMMENT ON COLUMN fact_reseller_sales.customer_po_number IS '客户po编号';
COMMENT ON COLUMN fact_reseller_sales.order_date IS '下单日期';
COMMENT ON COLUMN fact_reseller_sales.due_date IS '应付日期';
COMMENT ON COLUMN fact_reseller_sales.ship_date IS '发货日期';
COMMENT ON COLUMN fact_sales_quota.sales_quota_key IS '销售quota主键/外键标识';
COMMENT ON COLUMN fact_sales_quota.employee_key IS '员工主键';
COMMENT ON COLUMN fact_sales_quota.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_sales_quota.calendar_year IS 'calendar年份';
COMMENT ON COLUMN fact_sales_quota.calendar_quarter IS 'calendarquarter';
COMMENT ON COLUMN fact_sales_quota.sales_amount_quota IS '销售金额quota';
COMMENT ON COLUMN fact_sales_quota.date IS '日期';
COMMENT ON COLUMN fact_survey_response.survey_response_key IS '调查响应主键/外键标识';
COMMENT ON COLUMN fact_survey_response.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN fact_survey_response.customer_key IS '客户主键';
COMMENT ON COLUMN fact_survey_response.product_category_key IS '产品大类主键';
COMMENT ON COLUMN fact_survey_response.english_product_category_name IS 'english产品category名称';
COMMENT ON COLUMN fact_survey_response.product_subcategory_key IS '产品子类主键';
COMMENT ON COLUMN fact_survey_response.english_product_subcategory_name IS 'english产品subcategory名称';
COMMENT ON COLUMN fact_survey_response.date IS '日期';
COMMENT ON COLUMN new_fact_currency_rate.average_rate IS 'average比率';
COMMENT ON COLUMN new_fact_currency_rate.currency_id IS '货币id';
COMMENT ON COLUMN new_fact_currency_rate.currency_date IS '货币日期';
COMMENT ON COLUMN new_fact_currency_rate.end_of_day_rate IS 'endof天比率';
COMMENT ON COLUMN new_fact_currency_rate.currency_key IS '货币主键';
COMMENT ON COLUMN new_fact_currency_rate.date_key IS '日期主键/外键标识';
COMMENT ON COLUMN prospective_buyer.prospective_buyer_key IS 'prospectivebuyer主键/外键标识';
COMMENT ON COLUMN prospective_buyer.prospect_alternate_key IS 'prospect备用主键/外键标识';
COMMENT ON COLUMN prospective_buyer.first_name IS '第一次名称';
COMMENT ON COLUMN prospective_buyer.middle_name IS 'middle名称';
COMMENT ON COLUMN prospective_buyer.last_name IS '最后一次名称';
COMMENT ON COLUMN prospective_buyer.birth_date IS '出生日期';
COMMENT ON COLUMN prospective_buyer.marital_status IS '婚姻状态';
COMMENT ON COLUMN prospective_buyer.gender IS '性别';
COMMENT ON COLUMN prospective_buyer.email_address IS '电子邮箱';
COMMENT ON COLUMN prospective_buyer.yearly_income IS 'yearly收入';
COMMENT ON COLUMN prospective_buyer.total_children IS '总计children';
COMMENT ON COLUMN prospective_buyer.number_children_at_home IS '编号childrenathome';
COMMENT ON COLUMN prospective_buyer.education IS '教育程度';
COMMENT ON COLUMN prospective_buyer.occupation IS 'occupation';
COMMENT ON COLUMN prospective_buyer.house_owner_flag IS 'houseowner标记';
COMMENT ON COLUMN prospective_buyer.number_cars_owned IS '编号carsowned';
COMMENT ON COLUMN prospective_buyer.city IS 'city';
COMMENT ON COLUMN prospective_buyer.state_province_code IS 'stateprovince代码';
COMMENT ON COLUMN prospective_buyer.postal_code IS '邮政编码';
COMMENT ON COLUMN prospective_buyer.phone IS '电话';
COMMENT ON COLUMN prospective_buyer.salutation IS 'salutation';
COMMENT ON COLUMN prospective_buyer.unknown IS 'unknown';
COMMENT ON COLUMN sysdiagrams.name IS '名称';
COMMENT ON COLUMN sysdiagrams.principal_id IS 'principalid';
COMMENT ON COLUMN sysdiagrams.diagram_id IS 'diagramid';
COMMENT ON COLUMN sysdiagrams.version IS '版本';
COMMENT ON COLUMN sysdiagrams.definition IS 'definition';