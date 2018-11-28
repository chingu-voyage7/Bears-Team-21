$secret = 'SaboteurBears21'
$key = [Convert]::ToBase64String((1..32 |% { [byte](Get-Random -Minimum 0 -Maximum 255) }))
$encryptedSecret = ConvertTo-SecureString -AsPlainText -Force -String $secret | ConvertFrom-SecureString -Key ([Convert]::FromBase64String($key))

[System.Environment]::SetEnvironmentVariable("SABOTEUR_SECRET_KEY", $encryptedSecret, "Machine")