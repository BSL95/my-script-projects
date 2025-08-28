🔨 Password Cracking with John the Ripper

This section shows how to demonstrate the difference between weak and strong passwords using John the Ripper and a common wordlist.

1) Install John + a wordlist
Ubuntu / Debian / WSL
sudo apt update
sudo apt install john seclists -y


Wordlist path (RockYou):

/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt

Kali Linux

John is preinstalled. RockYou is at:

/usr/share/wordlists/rockyou.txt.gz


Decompress it:

sudo gzip -d /usr/share/wordlists/rockyou.txt.gz


If you can’t find RockYou, you can manually download it:

sudo mkdir -p /usr/share/wordlists
cd /usr/share/wordlists
sudo wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

2) Create a small test set of hashes

We’ll hash three weak passwords and one strong password using SHA-512 crypt (prefix $6$). This makes a realistic “local password” cracking demo.

# from your lab folder (e.g., lab-modules/password-security)

# Weak examples
echo "password"      | openssl passwd -6 -stdin >  hashes.txt
echo "Password123"   | openssl passwd -6 -stdin >> hashes.txt
echo "Summer2024!"   | openssl passwd -6 -stdin >> hashes.txt

# One strong random example (feel free to replace with one from your generator)
echo "N6!aWq$7Bz%1Yt" | openssl passwd -6 -stdin >> hashes.txt


Quick sanity check:

head hashes.txt


You should see lines that start with $6$ (that means SHA-512 crypt).

3) Crack with John (wordlist attack)
Ubuntu / Debian / WSL (seclists path)
john --wordlist=/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt hashes.txt

Kali (wordlists path)
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt


Tip: If you ever get a “format” error, let John auto-detect (as above).
If you do want to specify the format explicitly, use:

john --format=sha512crypt --wordlist=/path/to/rockyou.txt hashes.txt

4) Show cracked vs. uncracked
john --show hashes.txt


What you’ll see

Weak ones (e.g., password, Password123, Summer2024!) should crack quickly.

A long, random password from your generator likely won’t crack with a basic wordlist.

5) (Optional) Add rules to improve cracking

John’s built-in rules mutate words (add digits, change case, append symbols, etc.):

john --wordlist=/path/to/rockyou.txt --rules hashes.txt

Troubleshooting

“Unknown ciphertext format name requested”

Ensure your hashes start with $6$ (SHA-512 crypt).

Try without --format (let John detect).

Check available formats:

john --list=formats | grep 512


“No such file or directory” for rockyou

On Ubuntu/WSL, install seclists (path shown above).

On Kali, decompress /usr/share/wordlists/rockyou.txt.gz.

Or manually download to /usr/share/wordlists/rockyou.txt and point John there.

Very slow or nothing cracks

That’s actually the point for strong, random, long passwords.

Try shorter/guessable passwords to illustrate the difference, or enable --rules.
