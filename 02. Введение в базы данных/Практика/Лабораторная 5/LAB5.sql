select * from aircrafts;

select aircraft_code, aircrafts.model from aircrafts;

select model, "range" from bookings.aircrafts_data
where "range" < 5000;

select tickets.book_ref, tickets.passenger_id, tickets.passenger_name
from bookings.tickets
where  tickets.passenger_name like 'V%' 
or tickets.passenger_name like 'E%';

select flight_no, scheduled_departure, scheduled_arrival, 
departure_airport, arrival_airport
from bookings.flights
where departure_airport = 'DME'
	and arrival_airport in ('LED', 'KZN')
	and scheduled_departure between '2017-08-31' and '2017-09-01';


select 
	flight_no,
	scheduled_departure,
	scheduled_arrival,
	actual_departure,
	actual_arrival
from bookings.flights
where departure_airport = 'DME'
and actual_departure = NULL;

SELECT 
flight_no,
scheduled_departure,
scheduled_arrival,
actual_departure,
actual_arrival
from bookings.flights
where  departure_airport = 'DME'
	and actual_departure is NULL;

select 
flight_no,
scheduled_departure,
scheduled_arrival,
coalesce(actual_departure,'9999-12-31'),
coalesce(actual_arrival,'9999-12-31')
from bookings.flights
where  departure_airport = 'DME'
	and arrival_airport  = 'KZN';

SELECT 
flight_no,
scheduled_departure,
scheduled_arrival,
coalesce(actual_departure,'9999-12-31') as "Actual Departure",
coalesce(actual_arrival,'9999-12-31') "Actual Arrival"
from bookings.flights
where  departure_airport = 'DME'
	and arrival_airport  = 'KZN';

SELECT 
scheduled_departure,
flight_no,
COALESCE(actual_departure::varchar, 'CANCELED') as "Actual Departure"
from bookings.flights
where departure_airport = 'DME'
 and arrival_airport = 'KZN';


SELECT
	scheduled_departure,
	flight_no,
	departure_airport,
	arrival_airport
FROM bookings.flights
where departure_airport = 'DME'
ORDER BY arrival_airport;

select 
	scheduled_departure,
	flight_no,
	departure_airport,
	arrival_airport
FROM bookings.flights
where departure_airport = 'DME'
ORDER BY arrival_airport, scheduled_departure DESC;

SELECT DISTINCT
	departure_airport,
	arrival_airport
from bookings.flights
order by 1,2;

SELECT 
	scheduled_departure,
	'from ' || departure_airport::varchar || ' to '
	|| arrival_airport::varchar as Destination,
	status
from bookings.flights;

select 
	book_ref,
	substring(passenger_name from 1 for position(' 'in passenger_name)) as Name,
	substring(passenger_name from  position(' 'in passenger_name)) as Surname
from bookings.tickets;

select 
	AVG(amount) as Average,
	SUM(amount) as Summary
from bookings.ticket_flights
where fare_conditions = 'Economy';

select 
	COUNT(*)
from bookings.ticket_flights
where fare_conditions = 'Economy';

SELECT 
	 COUNT(*)
from bookings.flights
where COALESCE(actual_arrival::date,'2017-06-12') = '2017-06-12';

SELECT 
	 COUNT(actual_arrival)
from bookings.flights
where COALESCE(actual_arrival::date,'2017-06-12') = '2017-06-12';

SELECT 
	 COUNT(DISTINCT departure_airport)
from bookings.flights;

select
	flights.departure_airport,
	count(actual_arrival)
from bookings.flights
group by departure_airport;

select
	departure_airport,
	count(actual_arrival)
	from bookings.flights
	group by departure_airport
	having count(actual_arrival) < 50;

select
	departure_airport,
	arrival_airport,
	count(actual_arrival)
from bookings.flights
group by rollup (departure_airport, arrival_airport)
having count (actual_arrival) > 300;

select 
	departure_airport,
	arrival_airport,
	count(actual_arrival)
from bookings.flights
group by cube (departure_airport, arrival_airport)
having count(actual_arrival) > 300;