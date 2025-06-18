# Build-Phase
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

ENV ASPNETCORE_URLS=http://+:80

# Kopiere und restore Abhängigkeiten
COPY ToDoUi/*.csproj ./
RUN dotnet restore

# Kopiere den Rest des Codes und baue die App
COPY ToDoUi/. ./
RUN dotnet publish -c Release -o /out

# Laufzeit-Phase
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

COPY --from=build /out ./
ENTRYPOINT ["dotnet", "ToDoUi.dll"]

EXPOSE 80