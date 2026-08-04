-- ============================================================================
-- Pipeline Stage History Triggers
-- ============================================================================

drop trigger if exists pipeline_stage_history_insert on pipeline;

drop trigger if exists pipeline_stage_history_update on pipeline;

drop function if exists pipeline_stage_history_insert ();

drop function if exists pipeline_stage_history_update ();

-- ============================================================================
-- INSERT
-- ============================================================================

create function pipeline_stage_history_insert()
returns trigger
language plpgsql
as $$
begin
  insert into pipeline_stage_history (
    opportunity_id,
    talent_id,
    changed_by_id,
    to_stage
  )
  values (
    new.opportunity_id,
    new.talent_id,
    new.owner_id,
    new.stage
  );

  return new;
end;
$$;

create trigger pipeline_stage_history_insert
after insert
on pipeline
for each row
execute function pipeline_stage_history_insert();

-- ============================================================================
-- UPDATE STAGE
-- ============================================================================

create function pipeline_stage_history_update()
returns trigger
language plpgsql
as $$
begin
  insert into pipeline_stage_history (
    opportunity_id,
    talent_id,
    changed_by_id,
    to_stage
  )
  values (
    new.opportunity_id,
    new.talent_id,
    new.owner_id,
    new.stage
  );

  return new;
end;
$$;

create trigger pipeline_stage_history_update
after update of stage
on pipeline
for each row
execute function pipeline_stage_history_update();