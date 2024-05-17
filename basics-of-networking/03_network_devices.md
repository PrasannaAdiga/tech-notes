# Network devices

## Network Interface Cards (NICs)
- If a device needs to connect to internet, it atleast needs a single Network Interface Card
- The network adapter installed on your network device.
- Provides the physical and electrical, light or radio frequency connections to the network media.
- It can either be an expansion card, USB devices or built directly into the motherboard.

## Hubs 
- Used to Connect Devices Together Within a Network
- Used in Early Networks; Replaced by Switches
- “Multi-Port Repeater”
    - Traffic goes in one port and is repeated (broadcasted) out every other port
    - OSI Layer 1 Device
    - Dumb Network Device
    - Causes increased network collision errors
- Much Less Efficient than a Switch
- Legacy Equipment No Longer Used

## Switches
- Switches uses MAC addresses of each devices within our Local Area Network(LAN)
- Connects Devices Together Just Like a Hub
- Intelligent Network Device (OSI Layer 2)
- Memorizes the MAC Address of Each Device Connected to It via a MAC Address Table, sometimes called a Content Addressable Memory (CAM) Table
- Pays attention to Source and Destination MAC addresses during Communication Process
- Use Application-Specific Integrated Circuitry (ASIC), which makes them Extremely Fast
- Breaks up Collision Domains
    - Traffic Goes in One Port and Is Repeated out to Only Destination Port
    - Designed for High Bandwidth
    - Standard in Today’s Network Infrastructure

## Wireless Access Point (WAP)
- A wireless access point (WAP) is a bridge that extends the wired network to the wireless network.
- Just like a switch, it’s a Data Link Layer 2 device.
- Note: A WAP is not a router.

## Wireless Range Extender
- Extends the range of a wireless network by acting as a wireless repeater.
- Rebroadcasts radio frequencies from the wireless network it is associated with

## Routers
- Routers uses IP addresses to communicate between different network domains.
- Used to Connect Different Networks Together
- Routes Traffic Between Networks using IP Addresses
- Uses Intelligent Decisions (Routing Protocols) to Find the Best Way to Get a Packet of Information from One Network to Another.
- Break Up Broadcast Domains
- OSI Layer 3 Device
    - Layer 3 = Router 
    - Layer 2 = Switch 
    - Layer 1 = Hub

## Modems
- Modems modulate one signal to another, such as analog to digital.
- For example, modulating a telephone analog signal into a digital signal that a router can understand.    

## Small Office Home Office (SOHO) Device
- All-In-One Wireless Router with Expanded Capabilities:
    - Router, Wireless Access Point, Firewall, Switch, DHCP Server, NAT Device, File Server, etc.

## Media Converters
- Like its name implies, it converts one media type to another.
- Layer 1 Device: Performs physical layer signal conversion.
- Ethernet to fiber optic media converters are commonly use

## Firewalls
- Firewalls are the foundation of a defense-in-depth network security strategy.
- They protect your network from malicious activity on the Internet.
- Prevent unwanted network traffic on different networks from accessing your network.
- Firewalls do this by filtering data packets that go through them
- They can be a standalone network devices or software on a computer system, meaning network-based(hardware) host-based(software)

### Types of Firewalls

- Packet Filtering Firewalls
    - 1st Generation & Most Basic
    - Basic Filtering Rules
- Circuit-Level Firewalls
    - 2nd Generation
    - Monitors Valid/Invalid TCP Sessions
- Application Layer 7 (NGFW) Firewalls
    - 3rd Generation
    - Much more Advanced; Covered Later in Course

### DHCP Server
- Dynamic Host Configuration Protocol (DHCP) Server
- Automatically Assigns IP Addresses to Hosts
- Makes Administering a Network Much Easier
- An Alternative is Static IP addressing

### Voice over IP (VoIP) Endpoints
- Most phone systems run over IP networks via dedicated protocols, such as the Session Initiation Protocol (SIP), both in-home and office environments.
- VoIP endpoint devices are hardware devices (phones) or software, such as Cisco Jabber, that allow you to make phone calls.

### Ethernet Cable
- Ethernet is a network protocol that controls how data is transmitted over a LAN.
- It has both physical and logical components.
- It’s referred to as the Institute of Electrical and Electronics Engineers (IEEE) 802.3 Standard.
- It supports networks built with coaxial, twisted-pair, and fiber-optic cabling.
- The original Ethernet standard supported 10Mbps speeds, but the latest supports much faster gigabit speeds.
- Ethernet uses CSMA/CD(wired) & CSMA/CA(wireless) access methodology, which is the logical component.