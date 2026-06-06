# ApartmentOps IT Ops Hub

This repo contains the code skeleton for the ApartmentOps incident workflow.

## Goal

Convert service outages into structured incident tickets with optional AI summaries.

## Flow

Uptime Kuma
-> FastAPI Alert Bridge
-> Ticket CSV / SQLite
-> NVIDIA AI summary
-> Streamlit dashboard
-> Discord / Telegram notification

## Safety

This public repo uses fake data only. Real URLs, IPs, keys, webhook URLs, and incident logs belong in the private operations repo.
