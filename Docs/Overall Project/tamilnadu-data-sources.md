# Tamil Nadu Data Sources & Market Data Strategy

This document lists free data sources and strategies to collect market, weather, and soil data for Tamil Nadu (India). Use these sources during the MVP and prioritize local government feeds when available.

## Weather Data
- **Open-Meteo**: Free, global weather forecasts, historical data, and some agricultural parameters.
- **NASA POWER**: Global meteorological and solar radiation data useful for crop modeling and solar estimates.
- **IMD (India Meteorological Department)**: Primary country weather agency. Some data might be accessible via APIs or reports; check IMD’s website & local data access policies.
- **GFS/ECMWF**: Forecast model outputs for predictions.

## Soil & Land Data
- **SoilGrids (ISRIC)**: Global gridded soil properties (coarse but public); useful for preliminary recommendations.
- **FAO Global Soil Data**: Good for general soil properties and pH, organic carbon.
- **National Data**: Search for Tamil Nadu / Indian government soil maps & reports; NBSS & LUP (National Bureau of Soil Survey & Land Use Planning) produce nation-specific data which may be downloadable.

## Market Prices
- **eNAM**: National Agriculture Market — may have an API or public CSVs for daily mandi prices per commodity in India and Tamil Nadu; is a primary data source for market prices.
- **Agmarknet (Ministry of Agriculture & Farmers Welfare)**: Provides daily arrival & price data across `mandis` in India; public resources available for scraping or downloads.
- **Local Mandi Sites**: Tamil Nadu state mandi data might be published via state agricultural departments; this varies by state.

## Crop & Plant Data
- **FAO, ICAR**: Global and India-specific crop guidance (ICAR is Indian Council of Agricultural Research).
- **Tamil Nadu Agriculture Dept**: Check extension websites for localized guidance and crop calendars.

## Satellite & Imagery
- **Sentinel Hub / Copernicus**: Satellite imagery for farm imagery; complex for MVP but useful later for NDVI and change detection.
- **NASA Landsat**: Free Landsat imagery for analysis but complex for MVP.

## Market Price Scraping Strategy
1. Prioritize official sources (eNAM, Agmarknet) with public CSVs/APIs.
2. Build a `market_scraper` service that scrapes daily price tables, normalizes commodity names and units, and adds `market_prices` records in Supabase. Respect robots.txt and scraping terms.
3. Use a caching & dedup layer: use `source` + `market_date` + `commodity` as idempotent keys.

## Geographical Workflows & Localization
- Use Tamil Nadu administrative boundaries to map farm locations into districts & taluks; use Indian Census boundary shapefiles or GADM for mapping.
- Prefer using languages and units local to Tamil Nadu (e.g., Tamil language strings, units like Kg, Quintal where appropriate).

## Legal & Access Considerations
- Confirm that scraping public websites such as eNAM and Agmarknet is permitted in their terms of use.
- For datasets requiring registration or API usage, register and respect API usage limits.

## Next steps for Pilot
- Register API or download data from eNAM/Agmarknet and build a `market` service that aggregates pricing per commodity for Tamil Nadu.
- Seed the pilot Supabase database with known local crops and a sample dataset for the top 10 vegetables & grains in Tamil Nadu.
