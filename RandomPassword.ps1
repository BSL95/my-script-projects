function RandomPassword {
    param([int]$Length = 15)

    $lower  = "abcdefghijklmnopqrstuvwxyz"
    $upper  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    $digit  = "0123456789"
    $symbol = "!@#$%^&*()-_=+[]{};:<>,.?/\|`~"

    # Pick at least one from each
    $password = @(
        ($lower  | Get-Random -Count 1)
        ($upper  | Get-Random -Count 1)
        ($digit  | Get-Random -Count 1)
        ($symbol | Get-Random -Count 1)
    )

    # Fill the rest from the full pool
    $allChars = ($lower + $upper + $digit + $symbol).ToCharArray()
    $password += (1..($Length-4) | ForEach-Object { $allChars | Get-Random })

    # Shuffle so it’s not predictable
    -join ($password | Sort-Object {Get-Random})
}

# Calling the function
RandomPassword     
