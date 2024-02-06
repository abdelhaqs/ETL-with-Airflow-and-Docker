# Use the official PostgreSQL image from Docker Hub
FROM postgres:latest

# Create directories if needed and set permissions
RUN mkdir -p /pgbackup/SMAX \
    && mkdir -p /pgarchive/SMAX \
    && mkdir -p /pgdata/SMAX \
    && mkdir -p /pglog/SMAX \
    && chown -R postgres:postgres /pgbackup/SMAX \
    && chown -R postgres:postgres /pgarchive/SMAX \
    && chown -R postgres:postgres /pgdata/SMAX \
    && chown -R postgres:postgres /pglog/SMAX

# Optionally, you can specify additional configuration or initialization steps here