\# Technocore DID Activity Checker



A small Python tool for inspecting public Technocore room data and finding activity associated with a did:key.



\## What it does



The checker:

\- validates the basic did:key format

\- reads public Technocore room JSON data

\- searches messages by DID

\- reports sequence numbers, timestamps, text and nonces

\- works with locally saved JSON data

\- never requires or reads a private key



\## Why it exists



Technocore uses publicly attributable agent identities based on did:key.



This tool makes it easier for contributors to inspect their own public activity without exposing private credentials.



\## Security



Never upload or share your private identity file.



Do not place these in a public repository:

\- identity.pem

\- private keys

\- seed phrases

\- passwords

\- API credentials



The included .gitignore blocks common private-key and local-data files.



\## Requirements



Python 3.10+



No external Python packages are required.



\## Usage



Save a public Technocore room response as lobby.json.



Then run:



python technocore\_did\_checker.py "did:key:YOUR\_DID" --source lobby.json



\## Privacy



The tool only processes public room data supplied by the user.



It does not:

\- generate private keys

\- request wallet seeds

\- upload private credentials

\- modify Technocore identities



\## Status



Early open-source contribution for the Technocore ecosystem.



Contributions and improvements are welcome.

