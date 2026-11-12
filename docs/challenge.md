# Documento de referencia

Extracción de texto del PDF `challengeIoT_groupXX-1.pdf` (no incluye figuras).
El PDF completo, incluidas sus figuras, está en `docs/challengeIoT_groupXX-1.pdf`.
También se conserva el original en `~/challengeIoT_groupXX-1.pdf`.

SHA-256 del PDF: `6663f5522c24f3b578b6268c569975a0009054b33f0c4659a3bb932dbf9305cd`.

---

NaturePath
Inclusive IoT Trail Condition Monitoring System
IoT Challenge 2026–2027: Reconnecting with Nature

University of Deusto – Faculty of Engineering


Members:Hugo Arenaza, Kevin Saurel, Ruben Alonso
Submission date: October 15, 2026


1. Description of the IoT System and Its Purpose
1.1. The Problem

Access to natural environments is important for physical health, mental well-being, and
social inclusion. However, not everyone can enjoy these spaces under the same conditions.

People with reduced mobility, elderly citizens, and families with strollers often face obstacles
like standing water, slippery surfaces, and extreme weather. Most public parks lack real-time
condition updates, causing uncertainty that prevents people from visiting.

1.2. Our Solution: NaturePath
NaturePath is an IoT system designed to monitor environmental conditions along outdoor
trails and provide useful information to visitors.

Sensor stations collect and combine different measurements to evaluate trail conditions:

   ● Soil Moisture Sensor: Measures ground humidity.
   ● Water Sensor: Detects accumulated water at specific points.
   ● Temperature/Humidity Sensor: Monitors environmental conditions.
   ● Accelerometer: Estimates terrain inclination to identify potentially challenging
      slopes.
   ● Weather APIs: Provide rainfall forecasts and additional meteorological information.

The system combines these factors into an experimental Trail Condition Index, classifying
conditions into three levels: Green (Good), Yellow (Caution) and Red (Poor). Physical
indicators communicate the results at trail entrances without requiring smartphones.

The index provides environmental guidance rather than a guarantee of trail safety or
accessibility.


1.3. Long-Term Vision and MVP
Our long-term vision is a city-wide network of monitoring stations across Bilbao's parks.
During the course, we will develop an MVP using a Raspberry Pi 5, Grove sensors, Python
and an HTTP server. The prototype will initially use the available Soil Moisture Sensor, LCD,
LED, buzzer and push button. Additional sensors and weather API integration will be
incorporated depending on availability and development time.


2. Real-Life Use Case
Consider an elderly visitor planning a walk after several days of rain. NaturePath combines
soil moisture, water detection, terrain inclination and weather information to identify
potentially difficult trail conditions. For example, wet ground combined with a steep slope
may require additional caution.

The entrance indicator displays the calculated condition, helping the visitor decide whether
to continue or choose another route. Meanwhile, historical measurements help park
maintenance teams identify recurring environmental problems.

Value generated:

   ●   Greater confidence when planning outdoor activities.
   ●   Improved awareness of environmental and terrain conditions.
   ●   More inclusive access to nature.
   ●   Better information for park maintenance.
   ●   Reduced dependence on mobile applications.


3. Advantages Over Existing Solutions
Current navigation and accessibility platforms already provide useful information about
outdoor spaces.

Existing tools like Wheelmap or OpenStreetMap provide static accessibility or map data, but
do not reflect temporary conditions like flooding. NaturePath complements them with
continuously updated, local environmental sensing.

     Existing approach                Main limitation             NaturePath advantage

 Conventional maps             Mainly static geographical       Updated local sensor
                               information                      measurements

 Accessibility databases       May depend on user               Automated environmental
                               contributions                    observations

 Weather applications          Regional rather than             Measurements at relevant
                               path-specific information        path locations


 Visual inspection by         Requires manual visits          Continuous monitoring and
 maintenance teams                                            remote alerts



NaturePath represents an innovation rather than a new invention, as it combines existing IoT
technologies to provide real-time environmental information and improve access to natural
spaces.




4. Solution Architecture
The proposed architecture follows a layered IoT approach.




4.1. Sensing Layer
The sensing layer collects environmental data through a Soil Moisture Sensor, Water
Sensor, Temperature/Humidity Sensor and Accelerometer. These components measure


ground humidity, water presence, atmospheric conditions and terrain inclination. A push
button allows visitors to request information.

The MVP will initially use the available Soil Moisture Sensor, while additional sensors will be
integrated depending on availability.




4.2. Edge Processing Layer

The edge processing layer is based on a Raspberry Pi 5, which collects and processes
sensor measurements using Python. The system combines environmental data, terrain
inclination and available weather information to calculate an experimental Trail Condition
Index, classifying conditions as Good, Caution or Poor. It also controls local output devices
and prepares data for communication.

4.3. Communication Layer
In the MVP, the Raspberry Pi connects through Wi-Fi and shares data using an HTTP/REST
API. This allows the dashboard to access sensor measurements and trail status, while
external weather APIs, such as Euskalmet, can provide additional meteorological
information.

In the scalable version, LoRaWAN connects distributed sensor nodes to a gateway, while
MQTT enables efficient publish/subscribe communication between the network platform,
central server and connected devices.

4.4. Application Layer

The application layer includes the Flask web server, the local database, and the
monitoring dashboard. This layer is responsible for storing sensor measurements,
visualising current and historical data, and presenting the latest trail condition for monitoring
and analysis purposes.

4.5. User Interaction Layer

The user interaction layer communicates the trail condition directly to visitors through simple
physical feedback. In the MVP, this includes an LCD display to show the current status and
sensor information, together with an LED and a buzzer to provide immediate visual and
acoustic alerts. This approach allows the system to inform users without requiring them to
use a mobile application.

Scalable architecture: In the future version, multiple low-power outdoor sensor nodes could
be deployed at different trail locations. These nodes would transmit data through LoRaWAN
to a gateway/network server, which would then forward the data using MQTT to a central
server or cloud platform. From there, the system could update administrative
dashboards and entrance indicators across multiple monitored locations.


5. Sensors and Actuators
The MVP will use the following components. Additional sensors will be integrated depending
on availability.



                  Component                                       Purpose



 Raspberry Pi 5                                   Central processing and communication



 Grove Soil Moisture Sensor                       Measures ground moisture



 Grove Water Sensor (optional)                    Detects water accumulation



 Grove Temperature/Humidity Sensor (optional)     Measures environmental conditions



 Grove Accelerometer (optional)                   Estimates terrain inclination



 Push Button                                      Allows users to request information



 LCD Display                                      Shows trail conditions



 LED and Buzzer                                   Provide visual and acoustic feedback



 Grove connection board                           Connects sensors and actuators



The Soil Moisture Sensor will be the primary component of the MVP. Additional sensors will
improve the environmental assessment if available.




5.1. Analysis Logic
We propose a rule-based system that calculates an experimental Trail Condition Index
using available sensor measurements and weather information.


The system classifies conditions into three categories:

   ● Good: Favourable environmental conditions.
   ● Caution: Moderate moisture, inclination or unfavourable weather conditions.
   ● Poor: Combined factors suggesting significant difficulties, such as high moisture,
      standing water and steep terrain.

For example, wet and inclined surfaces may present greater difficulties than dry, flat
surfaces. An accelerometer installed and calibrated at a monitored location can help
estimate terrain inclination.

Thresholds will be determined experimentally. Sensor failures will trigger an unavailable
status. The index provides guidance rather than a guarantee of trail safety.




6. Physical and Link Layer Communication
Technologies
6.1. MVP Connectivity

The MVP uses the Raspberry Pi 5's built-in Wi-Fi within a controlled laboratory environment,
simplifying development.

6.2. Scalable Deployment

For broader outdoor deployments, LoRaWAN will be used for long-range, low-power
communication to forward sensor data via gateways to the central platform.

6.3. Power Supply

The MVP runs on USB-C power. Permanent installations will replace the Raspberry Pi with
low-power microcontrollers powered by rechargeable batteries and solar panels.

6.4. Outdoor Protection

Outdoor deployments will feature weather-resistant enclosures (IP-rated), sealed cabling,
vandal-resistant mountings, and accessible servicing points.


7. Application and Data Layer Communication
For the MVP, we will use HTTP/REST because it is already part of our practical laboratory
work.

Example endpoints:


       Endpoint                         Description

 GET                    Returns soil moisture data
 /api/moisture

 GET /api/water         Returns water detection information

 GET                    Returns temperature and humidity
 /api/environment       (optional)

 GET                    Returns terrain inclination (optional)
 /api/inclination

 GET /api/status        Returns the Trail Condition Index
                        classification

 GET /api/all           Returns all available measurements


Example JSON response:


  JSON‎
  {
      "node_id": "naturepath_01",
      "soil_moisture": "high",
      "status": "caution",
      "timestamp": "2026-10-15T14:00:00Z"
  }




For scalable deployments, MQTT publish/subscribe messaging will handle communication
between distributed nodes, gateways, indicators, and servers (e.g., topic:
naturepath/park01/node01/measurements).


8. Dashboard, Analytics and Open Data
8.1. Monitoring Dashboard
A Flask and SQLite dashboard will display sensor measurements, historical environmental
conditions and the Trail Condition Index. Grafana can be integrated for advanced
visualization.


8.2. Data Analytics
The system combines soil moisture, water detection, temperature, terrain inclination and
available weather forecasts to identify potentially unfavourable trail conditions. Historical
data may also help park maintenance identify recurring environmental problems.

8.3. Open Data Integration

External open data from Euskalmet (weather), Open Data Euskadi (air quality), and Bilbao
Open Data (parks and GIS) will complement local sensor observations in later releases.


9. Ethics, Privacy and Environmental Impact
9.1. Privacy

NaturePath monitors environmental conditions only, avoiding cameras, microphones, or user
tracking to ensure complete privacy.

9.2. Environmental Impact

IoT devices consume energy and require electronic components that have an environmental
footprint.

   ●   Low-power microcontrollers.
   ●   Energy-efficient wireless communication.
   ●   Durable, repairable enclosures.
   ●   Rechargeable batteries where appropriate.
   ●   Responsible recycling of electronic components.

9.3. Technology That Steps Aside

By using physical LED indicators, technology steps aside so visitors can enjoy nature
without screen distraction or app requirements.


10. Business Model Canvas
NaturePath follows a Business-to-Government (B2G) and Business-to-Institution (B2I)
model, targeting municipalities, universities and organisations responsible for managing
green spaces.

The main beneficiaries are citizens, particularly elderly people and those with reduced
mobility, while institutions are the potential paying customers.

Our value proposition focuses on reducing uncertainty about trail conditions, encouraging
outdoor activities and supporting park maintenance through environmental data.

The Business Model Canvas below summarises our key partners, activities, resources,
customer segments, costs and revenue streams.


10.1. Business Strategy

We propose an initial pilot in collaboration with the University of Deusto and potentially
Bilbao City Council to validate the solution before expanding to additional green spaces.

Our revenue model combines one-time installation fees with recurring subscriptions for
monitoring, maintenance and technical support. Public innovation and accessibility grants
could help finance initial deployments.

Following the Value Proposition approach, we identify three elements:

   ● Customer Jobs: Plan outdoor activities, assess trail conditions and maintain public
      green spaces.
   ● Pains: Uncertainty about environmental conditions, limited real-time information and
      difficulties identifying problematic areas.
   ● Gains: Greater confidence outdoors, improved accessibility awareness and more
      efficient maintenance decisions.

Value Validation: We hypothesise that visitors will find real-time trail information useful
when deciding whether to go outdoors. We will test this with a small prototype demonstration
involving 10–15 participants, measuring whether they understand the indicators and find the
information useful. Our initial success target is at least 80% correct interpretation and 70%
positive feedback.


11. SCRUM Planning and MVP Development
The project follows the SCRUM framework to ensure iterative development, rapid
prototyping, and continuous integration of hardware and software components across four
key sprints.



        Sprint                Focus Area              Key Deliverables & Objectives

 Sprint 1               Hardware & Sensor          Set up Raspberry Pi 5, calibrate the
                        Integration                Soil Moisture Sensor and integrate
                                                   Water, Temperature/Humidity and
                                                   Accelerometer sensors if available.

 Sprint 2               Data Processing & User     Implement the experimental Trail
                        Feedback                   Condition Index using available
                                                   measurements and connect LCD,
                                                   LED, buzzer and push button.

 Sprint 3               Communication &            Develop HTTP/REST API, SQLite
                        Dashboard                  database and Flask dashboard.
                                                   Explore weather API integration and
                                                   MQTT communication.

 Sprint 4               Integration & Evaluation   Perform end-to-end testing, validate
                                                   classification thresholds, simulate
                                                   different trail conditions and prepare
                                                   final documentation.


11.1. MVP Acceptance Criteria
The MVP will be considered successful when:

   1. The Raspberry Pi reads the Soil Moisture Sensor and any additional available
       sensors.
   2. The system processes environmental measurements and calculates the Trail
       Condition Index.
   3. The LCD displays the calculated condition, supported by LED and buzzer feedback.
   4. The HTTP server provides real sensor measurements in JSON format.
   5. A dashboard displays the latest measurements and status.
   6. The system handles invalid or unavailable sensor data.
   7. The complete sensing-to-feedback process can be demonstrated.

Advanced features such as LoRaWAN networking, solar power, and multi-node deployments
will remain part of the scalable architecture rather than mandatory MVP requirements.


12. References
   1. Raspberry Pi Foundation. Raspberry Pi Documentation – Getting Started.
       https://www.raspberrypi.com/documentation/computers/getting-started.html
   2. Euskalmet. Open Data and Meteorological Services.
       https://www.euskalmet.euskadi.eus/servicios/open-data/
   3. Open Data Euskadi. Public APIs.
       https://www.euskadi.eus/gobierno-vasco/-/apis-open-data/
   4. Bilbao City Council. Bilbao Open Data Portal.
       https://www.bilbao.eus/opendata/es/inicio
   5. Wheelmap. Wheelchair Accessibility Information.
       https://wheelmap.org/
   6. OpenStreetMap. Open Geographic Information Platform.
       https://www.openstreetmap.org/
   7. MQTT.org. MQTT Protocol Documentation.
       https://mqtt.org/
   8. The Things Network. LoRaWAN Documentation.
       https://www.thethingsnetwork.org/docs/
   9. Grafana Labs. Grafana Documentation.
       https://grafana.com/docs/
   10.Flask. Python Web Framework Documentation.
       https://flask.palletsprojects.com/


Conclusion
NaturePath demonstrates how IoT technology can help make natural environments more
accessible, inclusive and enjoyable. By combining environmental sensors, real-time data
processing and simple physical indicators, the system provides useful information about trail
conditions, helping visitors make informed decisions before going outdoors.

Starting with a realistic Raspberry Pi-based MVP, NaturePath offers the potential to expand
into a network of connected monitoring stations across Bilbao's green spaces.

Ultimately, our goal is simple: use technology to remove barriers to nature, encouraging
people to spend more time outdoors rather than in front of screens.
