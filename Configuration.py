# ========================================================================================================= #
# ========================================Kafka Connections =============================================== #
# ========================================================================================================= #
bootstrapServers = "cnt7-naya-cdh63:9092"
topic1 = 'api_to_spark'
topic2 = 'api_to_HDFS'
# ========================================================================================================= #
# ========================================booking api =============================================== #
url_search_location = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
url_search_hotels = "https://booking-com.p.rapidapi.com/v1/hotels/search"
headers = {
    "X-RapidAPI-Key": "25ca5bbe69msh35ccebd50e62d84p195705jsn4b55e5463832",
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}
querystring_loc = {"locale": "en-gb", "name": "Berlin"}
# ========================================================================================================= #
# =================================================telegram bot============================================ #
telegram_token = "5828356816:AAEiL7ObLZiHFUTvDvyH7RpNJdScRV-cNfc"
