# Generate a secure Django secret key for Windows users

function Generate-SecretKey {
    param(
        [int]$Length = 50
    )
    
    # Characters to use for the secret key
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?~|{}[]:;,.\/"
    
    # Convert to character array
    $charArray = $chars.ToCharArray()
    
    # Generate the secret key
    $secretKey = ""
    for ($i = 0; $i -lt $Length; $i++) {
        $randomIndex = Get-Random -Minimum 0 -Maximum $charArray.Length
        $secretKey += $charArray[$randomIndex]
    }
    
    return $secretKey
}

# Generate and display the secret key
$secretKey = Generate-SecretKey
Write-Host "Generated secret key: $secretKey"
Write-Host ""
Write-Host "Update your .env file with this key:"
Write-Host "SECRET_KEY=$secretKey"