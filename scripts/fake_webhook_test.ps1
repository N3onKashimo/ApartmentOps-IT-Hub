$Body = @{
    monitor = @{
        name = "Plex"
    }
    msg = "Plex is down in a simulated test"
    status = "down"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/webhook/uptime-kuma" `
    -ContentType "application/json" `
    -Body $Body
