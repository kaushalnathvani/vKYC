--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.15
-- Dumped by pg_dump version 10.11

-- Started on 2021-06-28 15:40:27 IST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 159908)
-- Name: agent_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agent_details (
    username character varying NOT NULL,
    password character varying NOT NULL,
    name character varying
);


ALTER TABLE public.agent_details OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 159934)
-- Name: queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queue (
    cust_name character varying NOT NULL,
    video_file_name character varying,
    image_name character varying,
    status character varying,
    added_date timestamp(0) without time zone
);


ALTER TABLE public.queue OWNER TO postgres;

--
-- TOC entry 2390 (class 0 OID 159908)
-- Dependencies: 185
-- Data for Name: agent_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agent_details (username, password, name) FROM stdin;
agent1	agent1	Agent 1
agent2	agent2	Agent 2
agent3	agent3	Agent 3
agent4	agent4	Agent 4
\.


--
-- TOC entry 2391 (class 0 OID 159934)
-- Dependencies: 186
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue (cust_name, video_file_name, image_name, status, added_date) FROM stdin;
Customer 1	2021-06-27 13/13/54_output.avi	2021-06-27 11/32/51.291540snap.jpg	Pending	2021-06-26 12:00:00
Customer 2	2021-06-27 10/21/49.181809output.mp4	2021-06-26 19/43/31.283969snap.jpg	In progress	2021-06-25 10:00:00
Customer 3	2021-06-24 18/57/00.980503output.mp4	2021-06-26 19/06/39.636738snap.jpg	Completed	2021-06-27 10:00:00
\.


--
-- TOC entry 2272 (class 2606 OID 159915)
-- Name: agent_details agent_details_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agent_details
    ADD CONSTRAINT agent_details_pk PRIMARY KEY (username);


-- Completed on 2021-06-28 15:40:27 IST

--
-- PostgreSQL database dump complete
--

