# from typing import List

# # IMPORTANT: keep this as one, long-lived list object.
# # We’ll mutate it in-place so any `from valid_emails import VERIFIED_SENDERS`
# # references see the refreshed contents.
# VERIFIED_SENDERS: List[str] = []

# def refresh_verified_senders(active_only: bool = True) -> List[str]:
#     """
#     Fetch emails from the database and replace the contents of VERIFIED_SENDERS
#     *in-place* so existing imports keep seeing the updated values.

#     Returns the refreshed VERIFIED_SENDERS.
#     """
#     try:
#         # Local import to avoid circulars and allow this module to be imported
#         # in environments where DB isn't available (e.g., tooling).
#         from database import fetch_authorized_sender_emails
#         emails = fetch_authorized_sender_emails(active_only=active_only)

#         # mutate in place; do NOT rebind the name
#         VERIFIED_SENDERS.clear()
#         VERIFIED_SENDERS.extend(emails)
#         return VERIFIED_SENDERS
#     except Exception as e:
#         # Don’t crash your app if DB is temporarily unavailable
#         print(f"(warn) refresh_verified_senders: DB fetch failed: {e}")
#         return VERIFIED_SENDERS  # whatever it had before (possibly empty)


# def get_verified_senders(active_only: bool = True) -> List[str]:
#     """
#     Convenience accessor. If the list is empty, refresh it once.
#     You can call this anywhere you currently use VERIFIED_SENDERS.
#     """
#     if not VERIFIED_SENDERS:
#         refresh_verified_senders(active_only=active_only)
#     return VERIFIED_SENDERS








VERIFIED_SENDERS = [
    # "muhammad.uzair@hayo.net",
    "rates@382com.com",
    "rates@42com-int.com",
    "rates@917consulting.net",
    "rates@acepeakinvestment.com",
    "sana@acepeakinvestments.com",
    "rates@acmetel.com",
    "rates@adctelecom.it",
    "rates@advisesrl.it",
    "rates@afinnaone.it",
    "rates@airontel.com",
    "rates@alizeetelecom.com",
    "rates@alkaip.com",
    "rates@allip-telecom.com",
    "rates@alltimetelecom.net",
    "rates@altmedia-telecom.ro",
    "purchasing@apelby.com",
    "vendor_rates@asiaat.com",
    "rates@awantel.com",
    "rates@bankai.net",
    "rates@belfonic.com",
    "Carrier.Pricelist@bics.com",
    "Antoine.Antoun@btc.com.bh",
    "rates@bhaoo.com",
    "Buy.rates@airtel.com",
    "route.test@airtel.com",
    "rates@bistalk.com",
    "rates@brilliantholdings.com",
    "rates@brmtelecom.com",
    "kim_ortega@brmtelecom.com",
    "karolay@brmtelecom.com",
    "rates@callcaribe.com",
    "pricing@carrieritalia.it",
    "asafor@013netvision.co.il",
    "purchasing.cz@cetin.cz",
    "idd@cmi.chinamobile.com",
    "chn_cmi_plr@live.ixlink.com",
    "voicesellrate@cmi.chinamobile.com",
    "voicebuyrate@cmi.chinamobile.com",
    "rate@chinaskyline.netl",
    "serena@chinaskyline.com",
    "rates@cimatelecom.com",
    "rates@mediatel.com",
    "rates@claritynetworks.com.au",
    "rates@commpeak.com",
    "rates@directo.com",
    "rates@confabtelecom.net",
    "notifications@coperato.com",
    "rates@cronostelecom.com",
    "carrier.rates@flatplanetphone.com",
    "rates@dataaccessvoip.com",
    "rates@datora.net",
    "rates@dawnglobal.net",
    "rates@dexatel.com",
    "rates@dialtel.net",
    "rates@didxl.com",
    "rates@digastelecom.com",
    "rates@dime.com.hk",
    "rates@directelco.com",
    "rate@qoolize.com",
    "account@easytermination.com",
    "rates@ecocarrier.com",
    "buyrates@etisalat.ae",
    "Voice.Rate@europeer.de",
    "rates@evox.fr",
    "buy@lancktele.com",
    "buy@lancktele.com",
    "tim@felixtelecom.com",
    "rates@first-sunrise.com",
    "rates@focustelecom.es",
    "rates@gabsgroup.com",
    "rates@gcn-tel.com",
    "rates@gencomtel.com",
    "rates_admin@gizatglobal.com",
    "rates@glmtelecom.com",
    "rates.gateway@gloworld.com",
    "globacomratesheets-importer@novatel.co.uk",
    "rates@globalreachmobile.com",
    "rates@global-voice.net",
    "mark_spencer2018@outlook.com",
    "rateadmin@globeteleservices.com",
    "rates@globtel.de",
    "rates@gomobit.com",
    "pricing.voip@go4mobility.com",
    "buy.rates@greenpacketglobal.com",
    "rates@hansatelecom.com",
    "rates@halo.co.il",
    "tariffs@hkbnes.net",
    "rates@hotmobile.co.il",
    "usa_ibas_plr@live.ixlink.com",
    "rates@iconnectglobal.com",
    "rates@ics-voice.net",
    "rates@identidadtelecom.net",
    "pm@globalcsinc.com",
    "rates@imctele.com",
    "sales@imctele.com",
    "rates@lingo.com",
    "ildrates@46labs.com",
    "rates@infotelecom.al",
    "rates@ingenuitytelecom.com",
    "rates@innovativetelecomcorp.com",
    "rates@ipbtel.com",
    "rates@ipvoip.net",
    "correspondence@iraqguru.com",
    "rates@jigsawtel.com",
    "rates@jigsawtel.com",
    "kt-pricing@kt.com",
    "sales@kwak-telecom.com",
    "Rates@lastmilecorp.com",
    "rates@latinatel.net",
    "rates@latcomm.net",
    "lebara@ascadeconnect.com",
    "ratemod@lexico-voip.com",
    "pricing@liquidtelecom.com",
    "rates@sinpin.com",
    "rbassil@mymada.com",
    "alouis@mymada.com",
    "rate@mainberg.net",
    "rates@manor.net",
    "sales@manor.net",
    "rates@mapletele.com",
    "sales@massend.co",
    "Mubasher.hussain@massend.co",
    "info@mavana.co.uk",
    "rates@mgi-management.com",
    "rates@voip.trade",
    "rates@mkelnetworks.com",
    "rates@mletatel.com",
    "rates@mmdsmart.com",
    "rates@mmdsmart.com",
    "Pricelist@mobik.com",
    "Pricing.gc@mtn.com",
    "pricing@bayobab.africa",
    "wmpricing@bayobab.africa",
    "rates@mycountrymobile.com",
    "rates@NewAllianceWC.com",
    "cogs@nexmo.com",
    "rates@nextcommunications.com",
    "rates@ngncorp.com",
    "ebitar@ngncorp.com",
    "rates@nobelglobe.com",
    "rates@spotel.ro",
    "accounts@occam.global",
    "rates@ocean-tel.uk",
    "rates@omtelentia.com",
    "rates@orphy.org",
    "rates@paitelecomm.com",
    "rates@phoenos.com",
    "rates@pricing-plusnet.de",
    "wholesales@plusnet.de",
    "buyrates@prime-tel.com",
    "rates@qatama.com",
    "qatama@rates.carrier.cloud",
    "rates@qgcommunications.com",
    "buy@quickdialusa.net",
    "rates@quickcomtel.com",
    "rates@rapidlinkusa.com",
    "rates@razatelecom.com",
    "rates@telefacil.com.mx",
    "pricelist@relario.com",
    "lirang@contaqt.com",
    "rates@ricochetglobal.com",
    "rates@rigelvoice.com",
    "Rates@rise-sol.com",
    "terminations@roketelkom.co.ug",
    "rates@rscom.ca",
    "marina@rscom.ca",
    "rates@saftelco.com",
    "rates@saifcall.net",
    "rates@saifglobal.net",
    "elena@samitel.com",
    "sales@samitel.com",
    "scaffnet.buy@scaffnet.com",
    "rates@shauntelecom.com",
    "sifysgp_ratemod@sifycorp.com",
    "sifysgp_ratemod@sifycorp.com",
    "rate@sigmatelecom.com",
    "ceren.talay@sigmatelecom.com",
    "rates@sipstatus.com",
    "rates@voiprates.biz",
    "rates@skylinkstelecom.com",
    "rates@softtop.tech",
    "rates@stanacard.com",
    "rates@swisslink-carrier.com",
    "rates@sygmatel.com",
    "rates@tnzi.com",
    "matthew.scott@tnzi.com",
    "rates@sync-sound.com",
    "carriers@synergybeam.com",
    "ratesheets@talk360.com",
    "o.ozalp@talk360.com",
    "rateadmin@proof.tatacommunications.com",
    "rates@techopensystems.co.za",
    "rates@telconnect.net",
    "rates@telebizint.com",
    "rates@telecall.com",
    "rating@telecelglobal.com",
    "numbering.plan@telecomitalia.it",
    "pricelist@tisparkle.com",
    "Rates@tele-geeks.net",
    "TGC.Voice-Rates@telekom.de",
    "rateadmin-telinhk@telin.net",
    "tariff@telemondo.biz",
    "prices@telia.lt",
    "rosemary.nwankwo@telko-ms.com",
    "rates@telmobil.net",
    "rates.update@teltacworldwide.com",
    "rates@telvantis.com",
    "rate.notification@termsat.com",
    "amit.eshel@tiebreak.dev",
    "rates@titanxwholesale.com",
    "ild_rate_notification@t-mobile.com",
    "voice.rates@toku.co",
    "irwyn.yoong@toku.co",
    "rates@toptelnetworks.com",
    "rates@turktelekomint.com",
    "wholesale.voice@turktelekomint.com",
    "rates@tweettele.com",
    "rates@twichinggeneraltrading.com",
    "adela@twichinggeneraltrading.com",
    "rates@ultranetgh.com",
    "ultranetgh@rates.carrier.cloud",
    "rates@unicorncommunication.com",
    "rates@uqsng.com",
    "rates@unicalltd.com",
    "rates@universalphone.co.za",
    "rates@usmatrix.com",
    "rates@vacotel.net",
    "rates@valuableinfocom.com",
    "rates@vasudev.com",
    "info@vazq.com",
    "sales@vazq.com",
    "ratemod@verscom.com",
    "rates@vespertelecom.com",
    "rates@viber.com",
    "rates@vincomm.net",
    "iclrates@vodafoneidea.com",
    "rates@voiceareus.co.uk",
    "Sell.Rates@Voipboxx.com",
    "rates@voiptogether.com",
    "RateChange@Vonage.com",
    "rates@vonage.com",
    "rates@vonip.net",
    "rates.hk@voxsolutions.co",
    "rates@voxmaster.com",
    "voxmasterbilling@gmail.com",
    "rates@voxpace.com",
    "rates@voxzi.com",
    "rates@voycetel.com",
    "rates@vsvoice.com",
    "rates@wateeninc.com",
    "cost.manager@wavecrest.eu",
    "Fabian.Goos@wavecrest.com",
    "TSRates@46labs.com",
    "rates@wicworldcom.com",
    "rates@wicworldcom-service.com",
    "sellrates@wicworldcom.com",
    "noc@widelymobile.com",
    "rateadmin@worldhubcom.com",
    "rate@worldtonetech.com",
    "rates@zaheentelecom.com",
    "rates@zenittelecommunication.com",
    "vijay@zoxyl.com",
    "commercial@we2stars.com",
]

# import re

# # Email validation regex (simplified RFC 5322)
# email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# # Separate valid and invalid emails
# valid_emails = [email for email in VERIFIED_SENDERS if email_pattern.match(email)]
# invalid_emails = [email for email in VERIFIED_SENDERS if not email_pattern.match(email)]

# # Print results
# print("✅ Valid Emails:")
# for email in valid_emails:
#     print(email)

# print("\n❌ Invalid Emails:")
# for email in invalid_emails:
#     print(email)
