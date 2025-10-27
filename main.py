import requests
import json
import time

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Your new bio text
BIO_TEXT = "Never look back if you have nothing to regret."

# Cookie string (copy from your browser)
COOKIE = "datr=YVytaAw85zvjs97TBwdp_8wB; sb=YVytaLLsqtAAyX3TeaTkVJfj; ps_l=1; ps_n=1; c_user=100055973888921; dpr=1.25; fr=1uUxDcdEe8WTotqST.AWeA860YpoucMQbxkAExEMbmV7G1JTbmw82OAWT6hLSmic2rfEQ.Bo_thL..AAA.0.0.Bo_thL.AWdFeXI8rMIqSqTnBEJCSxcC-Sc; xs=6%3A9r8bE9ehflWW6Q%3A2%3A1756191949%3A-1%3A-1%3A%3AAcWtT5OpLIYPnEvCAjAI6T5GPYq7eq0FUlECrvb-1jeH; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1761532200493%2C%22v%22%3A1%7D; wd=994x803"

# Your user ID (c_user from cookie)
USER_ID = "100055973888921"

# Facebook tokens (these expire, you'll need to update them)
FB_DTSG = "NAfttI_dm3-7e9NQRHXhlBGPQyja-Vo3PxKmjmNDNqNOH8GX4N62Q1A:6:1756191949"
X_FB_LSD = "Oz295dKFLKeJSkxpryem89"

# Profile URL (your Facebook profile username/ID)
PROFILE_REFERER = "https://www.facebook.com/ansu.rijal.399/"

# Other dynamic values (may need updating)
DOC_ID = "25117775041186361"
JAZOEST = "25202"

# Optional: Set to True to publish a story about bio update
PUBLISH_STORY = False

# ============================================
# REQUEST SETUP
# ============================================

def update_facebook_bio(bio_text, publish_story=False):
    """
    Updates Facebook bio using GraphQL API
    
    Args:
        bio_text (str): The new bio text
        publish_story (bool): Whether to publish a story about the bio update
    
    Returns:
        dict: Response from Facebook API
    """
    
    url = "https://www.facebook.com/api/graphql/"
    
    # Get current timestamp
    timestamp = int(time.time() * 1000)
    
    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "priority": "u=1, i",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "sec-ch-ua-full-version-list": '"Microsoft Edge";v="141.0.3537.99", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"19.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-asbd-id": "359341",
        "x-fb-friendly-name": "ProfileCometSetBioMutation",
        "x-fb-lsd": X_FB_LSD,
        "cookie": COOKIE,
        "Referer": PROFILE_REFERER
    }
    
    # Variables for the GraphQL mutation
    variables = {
        "input": {
            "attribution_id_v2": f"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,{timestamp},755453,190055527696468,,",
            "bio": bio_text,
            "publish_bio_feed_story": publish_story,
            "actor_id": USER_ID,
            "client_mutation_id": "1"
        },
        "hasProfileTileViewID": False,
        "profileTileViewID": None,
        "scale": 1,
        "useDefaultActor": False
    }
    
    # Body parameters
    body_params = {
        "av": USER_ID,
        "__aaid": "0",
        "__user": USER_ID,
        "__a": "1",
        "__req": "1m",
        "__hs": "20388.HYP:comet_pkg.2.1...0",
        "dpr": "1",
        "__ccg": "EXCELLENT",
        "__rev": "1028959457",
        "__s": "y7gud6:wund0h:f43o4j",
        "__hsi": "7565723155953771868",
        "__dyn": "7xeUjGU5a5Q1ryaxG4Vp41twWwIxu13wFwhUngS3q2ibwNwnof8boG0x8bo6u3y4o2Gwfi0LVEtwMw6ywIK1Rwwwg8a8462mcwfG12wOx62G5Usw9m1YwBgK7o6C1uwoE4G17yovwRwlE-U2exi4UaEW2au1jwUBwJK14xm3y11xfxmu3W3y261eBx_wHwUwc22-awLyESE2KwwwOg2cwMwhEkxebwHwKG4VUjwFg2fwxyo566k1fxC13xecwBwWzUfHDzUiBG2OUqwjVqwLwHwGwto461wweW2K3abxG6E5i",
        "__csr": "gccjlMB2RgHbb7NOaxc4Y8lEp3sh4cBPNa8ylOihtkzZNIIOFEtfkYyRmBGJR4paOqh2fn9uBREGtpWh4KjQy9qGVEyhflehEgZVAl4JqiIPGRmkB7ayB9gRHjBteXhrGWVHnhddaWFHGiFqAhp-LByRCLGpaqhoOp3aAjuBL_LyaBHCyVu9hml24qF68AAFmGzrKaim8ByQXB-qiQly8x5CJ5RzKdy5p_GU-699uy3Wx2aKHzUO8BxmidGK-Am9Bzo-9yE-WBKimiiESiihAgPK9FJqGcxB3HyFpQbBrz8WEqDCDzVKcAGULAG5bK49oO5F98y9BDGnV9-qKQVQ4rKuES49pXDCAUfoG2Gi4UN1mimKUy7U-bDWyFFoW4ohxi2qfwCg88a9FUW5ECeDyoiK8wxAz8izVEoAAwBwAxqexq2J2UhiwsoaK5XxSEf8O5UJa2m5bBwYGGwhE4S7819o8E3FBwIzEswFxmu78jG1myrUeoW1Gw4coO1xwhEaEf9m2G1kCQbA8684O8yS18wygKbQ2OQ4EnxK12w8S8HDw16y2y0eRg0a_816o3Aiw18G0eaw2OE5JpVE0AN0nXw3dE03rxwbK8m1xw6GKpwqobqge61oxzg2-w59EU9o761ByoB38y0dJo9X80ieU6m2S1OGiU0gpxl0i80EG2q8kw14U8U2czU0L69w5Cw3oQ8yojwmiwLxp04Ww8epw4xw8G09nw2gEK0a2w0Djweqaw2uE52m0tmpw25omg3uwnE5Xggx24P01YK0i-0d2w3981_VC0a5o3Sw3mBByofUK8ymbCl1z5iV_9g1jS0UUd82pwjEkwgaDyE0PG",
        "__hsdp": "gay1cgQgzEgz8fSxahxa4aiW8zGyC8xkYiG2y5GoIaFgoEiwL6FEW22i5E8NWfcSx4G4gn61v5Fzzsn3Ar9NsNbd7jQw84reyEkxLiKyPh25h7NisgBNsIiyXAaxUPh9QmgKAQW9ouUNl5EhchNqaAgQcEmyFBF89jM_n9Hifcgoxi1kNsmB8iy89EoJEkTcAxKkQnl7W8DcEBiCHiKmF9mimG2EUApamHAAAAihA8V37G8vy4AaiDGEy9xxUOaa9hFUB4rAFkch9VcNA82918ycxbyx09pbxK4apa5xhBQqiUhjaIg2K9emcAzkegOUgm4FrpHmS3e9pBaQdhUYwa94cy4bwkowBxl4F38W694fAQ4-A2mUkGfKayoK15CDhq9WgdYZ38RpUx4wWwqodUdoyV9FVaAByojzo-3m75zVVoF7c4orGU4fzoKcxi11wiETU89Gg32CwWxu3m6oHwTx2327o5KHDxe2hHQicxxobHBK2613xe5EvByUO3a7E5W227o9oPptpUdUSGoy7U9oswr8yu6Hx268y2u4UW1sCDo8oO1Hwk8886a0FoO4o98469y85m3229otwi8d86W0wUrK5FWzUnxWEkQEcpp84q3O6o2Yy8S0PEO2q0SU6W1awsaxi1Qw65w5fx-6o2twkU461cwzAxOiewEwNwfqq1pwai0IEkw8G1mwoo4a68O1nwm82UwoE7a5EcoC1DxO2e6FE7O1Mx64o4W19w56wVU520ma13x21jwaK0mC1ewby0C827weG16G1Yw-waq6ohg9Eb816oy5Eco5m8wu82ZwCw42x90pEswBw45wsEW48Ki0g62y3a2m58sxd7wFxO0A8mw9u0H8jwLwuE2gwd22a",
        "__hblp": "1a5k3KAX5aQ1Tx-3K7S482FwhonwABgaF6220hWq78dEeE4um7oeawn8bo6S1WwCxS7kq5Ux0u89E6WUozpEtBwBCxW2W4oKbz8mxa221DwNxa22cy88o2pwDwgo985t0_xyq5U7u1HwtojwNwTw-y8Wuimi68SfwRx-2y7U5u48Sbz8kBjgdo5O486G1VwWwpAcwTx64E2dyUvwxyQ5UgwTwHwgUjxq7UeU985K5E721swkUswgUa8y1pwDw8qtwywYCwamdwl82hxe0xoCawkU8Uce7o4y488U6W2O1mw-xa13wc248pxO0B8Gdy85y5u3W4WwXw861cz86e10xi1MG586K8wKxO0YU4m6oy1GwaKicG226oqwdq8wUwj84miewQwBwfqq3W6Ebo7q9wa2782awlEsxt288Eb8lAxecwlU5y0K865o725Ec49xS8wg8sCxO6FE7O1MwzwjEO3O0S82DUb46VEaUaE9EG6HxZ2orGawpo4e485fwtEcE6C0RU9U4W0K86O2qi1fx-5awZwaO7U9Gx-1sw-w9-q6ohg9Eb83Uwwy8mwNwgXzpqwu82ZwCweC68ig2FwvU2yCwjEW48Ki0Y9EC2y1oxi78jhUaosw925E2nwvUK224U2BABylwvpFQ2qbxW2C1lx608wwCy8",
        "__sjsp": "gay1cgQgzEgz8fSxahxa4aiW8zGyC8xkYiG2y5GoIaFgoEiwL6FEW22i5EmhhXcyJFnOEhMzf2hzMHb5NqoUP5MV6OsnciPhTbi0whyeycRErQHEIQgxltKxasXmzrGZBGEbp9Q49V8eEppAZdfh95u4q8faimu9UaVSbcGgAPzC13zql1kV69rgKTwAgCm6Tyotp8yg9zBNCczp94Ap28847of42x1yl4y8lzcMhwAwIc2u1ygbOwrkeg8k2K17wqQ5k0wQ0ll00FBw",
        "__comet_req": "15",
        "fb_dtsg": FB_DTSG,
        "jazoest": JAZOEST,
        "lsd": X_FB_LSD,
        "__spin_r": "1028959457",
        "__spin_b": "trunk",
        "__spin_t": str(int(time.time())),
        "__crn": "comet.fbweb.CometProfileTimelineListViewRoute",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "ProfileCometSetBioMutation",
        "server_timestamps": "true",
        "variables": json.dumps(variables),
        "doc_id": DOC_ID
    }
    
    # Convert body params to URL-encoded string
    body = "&".join([f"{k}={v}" for k, v in body_params.items()])
    
    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        
        print("✅ Request sent successfully!")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # Print first 500 chars
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("Facebook Bio Update Script")
    print("=" * 50)
    print(f"\n📝 New Bio: {BIO_TEXT}")
    print(f"👤 User ID: {USER_ID}")
    print(f"📢 Publish Story: {PUBLISH_STORY}")
    print("\n🚀 Sending request...")
    print("-" * 50)
    
    result = update_facebook_bio(BIO_TEXT, PUBLISH_STORY)
    
    if result:
        print("\n✅ Bio update completed!")
    else:
        print("\n❌ Bio update failed. Check your tokens and cookies.")