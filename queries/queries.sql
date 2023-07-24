--total medals per country/year
select
  noc as country,
  year,
  count(1) as medals
from
  contestants
where
  medal is not null
group by
  noc,
  year;

--all contestants with medal
select
  noc as country,
  year,
  games,
  season,
  sport,
  event,
  medal
from
  contestants
where
  medal is not null;

--olympic countries with no population match
select
  distinct c.noc
from
  contestants c
  left outer join populations p on c.noc = p.country_code
where
  p.country_code is null;

--remove blank country code records
delete from country_codes where noc = '';

--miscellaneous
select
  count(1)
from
  contestants
where
  medal is null;