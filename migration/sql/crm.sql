create extension if not exists citext; -- text 衍伸，會把字母大小寫視作一樣
create extension if not exists pgcrypto; -- 提供 uuid 生成

-- bool: is_, has_, ...

drop table if exists note cascade;
drop type if exists note_target_type;


-- ==========================================================================================
-- NOTE
-- ==========================================================================================

create type note_target_type as enum (
  'talent',
  'client',
  'opportunity'
);


create table note (
  id integer generated always as identity primary key,

  target_type note_target_type not null,
  target_id text not null,

  created_by_id integer not null references users(id),

  content text not null,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- project/
-- ├── database/
-- │   └── migrations/
-- │
-- ├── seeds/
-- │   └── taxonomy/
-- │       ├── industry.json
-- │       └── function.json
-- │
-- └── scripts/
--     └── import_taxonomy.py

drop table if exists function_node cascade;
drop table if exists industry_node cascade;


-- ==========================================================================================
-- INDUSTRY NODE
-- ==========================================================================================


create table industry_node (
  id smallint generated always as identity primary key,

  parent_id smallint references industry_node(id),

  name text not null,

  is_active boolean not null default true,

  sort_order smallint not null default 0,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint industry_node_name_unique
    unique(parent_id, name)
);


create index idx_industry_node_parent_lookup
on industry_node(parent_id);


-- ==========================================================================================
-- FUNCTION NODE
-- ==========================================================================================

create table function_node (
  id smallint generated always as identity primary key,

  parent_id smallint references function_node(id),

  name text not null,

  is_active boolean not null default true,

  sort_order smallint not null default 0,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint function_node_name_unique
    unique(parent_id, name)
);


create index idx_function_node_parent_lookup
on function_node(parent_id);

drop table if exists users cascade;
drop type if exists user_role;
drop type if exists user_status;

create type user_role as enum (
  'consultant',
  'manager',
  'admin'
);

create type user_status as enum (
  'active',
  'invited',
  'suspended'
);

create table users (
  id integer generated always as identity primary key,

  name varchar(50) not null,
  email varchar(50) not null unique,
  role user_role not null,
  status user_status not null default 'active',

  create_at timestamptz not null default now()
);

delete from users;


-- Company Search Flow

-- 1. 顧問於 Client / Talent 建立流程中輸入公司名稱

-- 2. Frontend 第一次進入 company search 時：
--    - Query valid_company
--    - 將 valid_company 結果存入 frontend cache

-- 3. 顧問輸入公司名稱：
--    - 優先使用 frontend cache 搜尋 valid_company
--    - 找到對應公司：
--        → 使用 valid_company id 建立關聯

-- 4. 若 valid_company 搜尋無結果：
--    - 不立即觸發 company_raw search
--    - 等待顧問主動選擇「搜尋其他公司」
--    - Frontend 發送 request 至 backend

-- 5. Backend 搜尋 company_raw：

--    A. 找到可能匹配資料：
--       - 回傳 company_raw 候選
--       - 顧問確認是否為同一公司
--       - 若確認：
--           → 使用既有 raw mapping / 後續 review 流程

--    B. 無匹配資料：
--       - 顯示「是否新增公司」
--       - 顧問確認後：
--           → Insert company_raw
--           → 更新 backend company_raw cache

drop table if exists company_raw cascade;
drop table if exists company cascade;
drop table if exists company_alias cascade;
drop type if exists company_raw_status;

create type company_raw_status as enum (
  'pending', -- 等待季度整理
  'resolved', -- 已找到 company，建立 alias 關聯
  'ignored' -- 保留原始紀錄，但不參與 search engine
);

-- 顧問直接丟進去的資料
create table company_raw (
  id integer generated always as identity primary key,

  name text not null unique,
  
  status company_raw_status not null default 'pending',

  created_by_id integer not null references users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- 定義問題!! 如出現地區無所屬法定名稱 or 地區本身橫跨兩個國家則須討論定義處理 (但邏輯上不會改到架構)
create table company (
  id integer generated always as identity primary key,

  law_name citext not null,
  location text not null, -- TODO: 需決定地區 enum or 多值 ... ANS: 直接純文字
  tax_id text not null,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table company_alias (
  company_id integer not null references company(id),
  name citext not null,
  primary key(company_id, name),

  created_at timestamptz not null default now()

  -- 是否 unique name，就看 不同 company 會不會有相同的簡稱
);

comment on column company.location is '公司所在地；海外記錄國家，台灣可多記錄縣市';

drop table if exists talent_education cascade;
drop table if exists talent_function cascade;
drop table if exists talent_industry cascade;
drop table if exists talent_note cascade;
drop table if exists talent_source cascade;
drop table if exists talent cascade;

drop type if exists education_status cascade;
drop type if exists education_level cascade;
drop type if exists talent_status cascade;
drop type if exists expected_salary_status cascade;
drop type if exists candidate_sex cascade;
drop type if exists talent_source_type cascade;


-- ==========================================================================================
-- ENUM
-- ==========================================================================================

create type talent_source_type as enum (
  'import',    -- 匯入
  'platform',  -- 人才網站
  'other'      -- 其他
);
-- source logic
-- creater type     name
-- System  platform 104


create type talent_status as enum (
  'unknown',   -- 未知
  'hired',     -- 成功 Offer
  'open',      -- 考慮機會
  'archived',  -- 現狀穩定
  'active'     -- 積極求職
);


create type expected_salary_status as enum (
  'negotiable',     -- 面議
  'company_policy'  -- 依公司規定
);


create type candidate_sex as enum (
  'male',
  'female'
);

create type education_level as enum (
  'secondary',  -- 高中職 / high school
  'associate',  -- 副學士 / 專科 / 大專
  'bachelor',   -- 學士 / 本科
  'master',     -- 碩士
  'doctorate',  -- 博士
  'other'       -- 其他
);

create type education_status as enum (
  'unknown',    -- 未知
  'completed',  -- 已完成
  'studying',   -- 就讀中
  'withdrawn'   -- 肄業
);



-- ==========================================================================================
-- TALENT SOURCE
-- ==========================================================================================

create table talent_source (
  id integer generated always as identity primary key,

  type talent_source_type not null,
  name text not null,

  constraint talent_source_unique
    unique(type, name)
);


-- ==========================================================================================
-- TALENT
-- ==========================================================================================

create table talent (
  id uuid primary key default gen_random_uuid(),

  -- owner / source
  created_by_id integer not null references users(id),
  source_id integer not null references talent_source(id),

  -- basic info
  name_english text,
  name_chinese text,

  -- contact
  email citext unique,
  phone_country_code varchar(3) check (phone_country_code ~ '^[0-9]+$'),
  phone_number varchar(14) check (phone_number ~ '^[0-9]+$'),
  phone_extension varchar(10) check (phone_extension ~ '^[0-9]+$'),

  -- urls
  cv_url text,
  linked_urls text,
  ps_url text,

  -- career
  company_id integer references company(id),
  company_raw_id integer references company_raw(id),
  company_confidential boolean not null default false,
  current_title text,
  current_salary integer check (current_salary >= 0),

  -- preference
  status talent_status,
  expected_salary integer check (expected_salary >= 0),
  expected_salary_status expected_salary_status,

  -- personal
  sex candidate_sex,
  birth_year smallint check (birth_year between 1900 and 2900),
  birth_month smallint check (birth_month between 1 and 12),
  birth_day smallint check (birth_day between 1 and 31),

  -- education
  highest_education education_level,
  highest_school text,
  highest_major text,

  -- audit
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  -- company valid / raw 不可同時存在
  constraint talent_company_reference_check
    check ((company_id is null) or (company_raw_id is null)),

  -- 國碼 + 號碼避免重複
  constraint talent_phone_unique
    unique(phone_country_code, phone_number),

  -- 至少要有名字
  constraint talent_name_required_check
    check (
      name_english is not null
      or name_chinese is not null
    ),

  -- 至少一種聯絡方式
  constraint talent_reachable_check
    check (
      phone_number is not null
      or email is not null
      or cv_url is not null
    ),

  constraint talent_birth_month_day_check
    check ((birth_month is null) = (birth_day is null)),

    constraint talent_company_confidential_check
      check (
        company_confidential = false
        or (company_id is null and company_raw_id is null)
      )
);


comment on column talent.status is '求職狀態';
comment on column talent.current_title is '當前職位';
comment on column talent.current_salary is '當前年薪';
comment on column talent.expected_salary is '期望年薪';
comment on column talent.source_id is '人才來源';
comment on column talent.phone_country_code is '國碼';
comment on column talent.phone_number is '號碼';
comment on column talent.phone_extension is '分機';


-- ==========================================================================================
-- TALENT NOTE
-- ==========================================================================================


create table talent_note (
  id integer generated always as identity primary key,

  talent_id uuid not null references talent(id) on delete cascade,
  created_by_id integer not null references users(id),

  content text not null,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);


-- ==========================================================================================
-- TALENT INDUSTRY/FUNCTION
-- ==========================================================================================



create table talent_industry (
  talent_id uuid not null references talent(id) on delete cascade,
  industry_id smallint not null references industry_node(id),

  primary key(talent_id, industry_id)
);

create table talent_function (
  talent_id uuid not null references talent(id) on delete cascade,
  function_id smallint not null references function_node(id),

  primary key(talent_id, function_id)
);


create index idx_talent_industry_lookup
on talent_industry(industry_id);

create index idx_talent_function_lookup
on talent_function(function_id);


-- ==========================================================================================
-- TALENT EDUCATION
-- ==========================================================================================



create table talent_education (
  id integer generated always as identity primary key,

  talent_id uuid not null references talent(id) on delete cascade,

  school text not null,
  degree education_level,
  major text,

  status education_status not null default 'unknown',

  start_year smallint check (start_year between 1900 and 2900),
  start_month smallint check (start_month between 1 and 12),

  end_year smallint check (end_year between 1900 and 2900),
  end_month smallint check (end_month between 1 and 12),

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  -- 月份不可獨立存在
  constraint talent_education_month_year_check
    check (
      (start_month is null or start_year is not null)
      and
      (end_month is null or end_year is not null)
    ),

  -- 就讀中 / 未知可以沒有結束時間，其餘狀態需要結束時間
  constraint talent_education_status_check
    check (
      status in ('unknown', 'studying')
      or end_year is not null
    ),

  -- 結束時間不可早於開始時間
  constraint talent_education_period_check
    check (
      start_year is null
      or end_year is null
      or end_year > start_year
      or (
        end_year = start_year
        and (
          start_month is null
          or end_month is null
          or end_month >= start_month
        )
      )
    )
);

drop table if exists client_function cascade;
drop table if exists client_industry cascade;
drop table if exists client_contact cascade;
drop table if exists client cascade;

drop type if exists client_status;


-- ==========================================================================================
-- ENUM
-- ==========================================================================================

create type client_status as enum (
  'lead',      -- 加入觀察名單
  'ongoing',   -- 開發中
  'open'       -- 已簽約
);


-- ==========================================================================================
-- CLIENT
-- ==========================================================================================

create table client (
  id integer generated always as identity primary key,

  -- owner
  created_by_id integer not null references users(id),
  sales_owner_id integer references users(id),

  -- company
  company_id integer references company(id),
  company_raw_id integer references company_raw(id),

  -- status
  status client_status not null default 'lead',

  note text,

  -- audit
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  -- company valid / raw 不可同時存在
  constraint client_company_reference_check
    check (not (
        company_id is not null
        and company_raw_id is not null
    ))
);


-- ==========================================================================================
-- CLIENT CONTACT
-- ==========================================================================================

-- TODO: add trigger 保證 兩者 company id 一樣 
create table client_contact (
  id integer generated always as identity primary key,

  client_id integer not null references client(id),
  talent_id uuid not null references talent(id),

  created_by_id integer references users(id) on delete set null,

  is_active bool not null default true,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint client_contact_unique
    unique(client_id, talent_id)
);


comment on column client_contact.is_active is '客戶聯繫人的聯繫狀態';


-- ==========================================================================================
-- CLIENT INDUSTRY/FUNCTION
-- ==========================================================================================

create table client_industry (
  client_id integer not null references client(id) on delete cascade,
  industry_id smallint not null references industry_node(id),

  primary key(client_id, industry_id)
);


create index idx_client_industry_lookup
on client_industry(industry_id);

drop table if exists opportunity_function cascade;
drop table if exists opportunity_industry cascade;
drop table if exists opportunity cascade;

drop type if exists opportunity_status;


-- ==========================================================================================
-- ENUM
-- ==========================================================================================
-- 失敗
-- 進展中/成功/暫停/客戶自行找到／競爭對手找到 / 客戶無需求 
create type opportunity_status as enum (
  'ongoing', -- 進展中
  'failed', -- 失敗
  'placed', -- 成交
  'pending' -- 暫停
);

-- TODO: 新增一個 bool 表達是否已開票完成?
-- 其他未知狀況： LONG LIST 仍不知去向

-- client 必須簽約才可以開職缺
-- 但應該不用特別考慮後續取消簽約的狀態


-- ==========================================================================================
-- OPPORTUNITY
-- ==========================================================================================

create table opportunity (
  id integer generated always as identity primary key,

  created_by_id integer references users(id),

  client_id integer not null references client(id),
  client_contact_id integer not null references client_contact(id),

  -- basic info
  title text not null, -- 職缺名稱
  location text not null, -- 工作地點

  description text not null, -- 描述職缺的要求 細項等..
  headcount integer not null check (headcount > 0), -- 人數需求

  -- status
  status opportunity_status not null default 'ongoing', -- 預先假設會被加進 db 就是已經談好正在進行中
  is_priority boolean not null default false,

  opened_at timestamptz not null, -- 開始時間

  note text,

  -- audit
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);


-- ==========================================================================================
-- OPPORTUNITY INDUSTRY/FUNCTION
-- ==========================================================================================

create table opportunity_industry (
  opportunity_id integer not null references opportunity(id) on delete cascade,
  industry_id smallint not null references industry_node(id),

  primary key(opportunity_id, industry_id)
);


create table opportunity_function (
  opportunity_id integer not null references opportunity(id) on delete cascade,
  function_id smallint not null references function_node(id),

  primary key(opportunity_id, function_id)
);


create index idx_opportunity_function_lookup
on opportunity_function(function_id);

create index idx_opportunity_industry_lookup
on opportunity_industry(industry_id);

drop table if exists pipeline_stage_history cascade;
drop table if exists pipeline cascade;

drop type if exists pipeline_stage;


-- ==========================================================================================
-- ENUM
-- ==========================================================================================

-- 0728 向 Dave 了解完 pipeline_stage 的細節，了解到 Candidate Call 算是紀錄在
-- talent_note table 上面的行為，而不太算 pipeline_stage 的業務流程。
-- 因此考慮 talent_note 增加 contact type {"Candidate Call"}，而 pipeline_stage 移除。
-- 沒有人選 深綠色
-- 關閉 紅色
-- 面試中 黃色
-- 推簡歷 綠色 加入職缺



create type pipeline_stage as enum (
  'added', -- 將人選加入文件項目裡 (default value)
  'II', 'PS', 'CI', 'PF', 'PO', 'SW', -- 業務流程
  'fail', 'split'
  -- 'Candidate Call', -- 陌生人選電話，知道基本資料30s，算業務流程但只能是一種標記，且不一定要再 pipeline 因為資料屬於 talent
  -- 'Split', -- 開票；應該是在 opportunity 標記才對，例如 SW 才可以標記 Split
);


-- ==========================================================================================
-- PIPELINE'
-- ==========================================================================================

create table pipeline (
  opportunity_id integer not null references opportunity(id),
  talent_id uuid not null references talent(id),

  primary key(opportunity_id, talent_id),

  owner_id integer not null references users(id),

  stage pipeline_stage not null default 'added',

  stage_entered_at timestamptz not null default now()
);


-- ==========================================================================================
-- PIPELINE STAGE HISTORY
-- ==========================================================================================

create table pipeline_stage_history (
  id integer generated always as identity primary key,

  opportunity_id integer not null references opportunity(id),
  talent_id uuid not null references talent(id),

  changed_by_id integer not null references users(id),

  to_stage pipeline_stage not null,

  created_at timestamptz not null default now(),

  constraint pipeline_stage_history_pipeline_fk
    foreign key(opportunity_id, talent_id)
    references pipeline(opportunity_id, talent_id)
);


create index idx_pipeline_talent_lookup
on pipeline(talent_id);