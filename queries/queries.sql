--total medals per country/year
select
  p.country,
  cc.iso3 as country_code,
  count(1)
from
  contestants c
  join country_codes cc on c.noc = cc.noc
  join populations p on cc.iso3 = p.country_code
where
  c.year >= 1960
  and c.year <= 2016
  and c.medal is not null
group by
  p.country,
  cc.iso3
order by
  country asc;

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