import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def sanctum():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT')
    )
    def call_api(url):
        try:
            response = requests.get(url)
            # Check if request was successful
            if response.status_code == 200:
                return response.json()
            else:
                print("Error:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

    def print_data(data):
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        for key in data["apys"]:
            for token in liquid_staking:
                if key == token["key"]:
                    rounded_rate = round(data["apys"][key] * 100,2)
                    cursor.execute("INSERT INTO defi_yield (yield_id, rate) VALUES (%s, %s)", (token["id"], rounded_rate))
                    conn.commit()


    liquid_staking = [
        {'key':'5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm', 'name':'INF', 'id':'108'},
        {'key':'BonK1YhkXEGLZzwtcvRTip3gAL9nCeQD7ppZBLXhtTs', 'name':'bonkSOL', 'id':'109'},
        {'key':'bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1', 'name':'bSOL', 'id':'110'},
        {'key':'CgnTSoL3DgY9SFHxcLj6CgCgKKoTBr6tp4CPAEWy25DE', 'name':'cgntSOL', 'id':'111'},
        {'key':'GRJQtWwdJmp5LLpy8JWjPgn5FnLyqSJGNhn5ZnCTFUwM', 'name':'clockSOL', 'id':'112'},
        {'key':'Comp4ssDzXcLeu2MnLuGNNFC4cmLPMng8qWHPvzAMU1h', 'name':'compassSOL', 'id':'113'},
        {'key':'Dso1bDeDjCQxTrWHqUUi63oBvV7Mdm6WaobLbQ7gnPQ', 'name':'dSOL', 'id':'114'},
        {'key':'edge86g9cVz87xcpKpy3J77vbp4wYd9idEV562CCntt', 'name':'edgeSOL', 'id':'115'},
        {'key':'he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A', 'name':'hSOL', 'id':'116'},
        {'key':'HUBsveNpjo5pWqNkH57QzxjQASdTVXcSK7bVKTSZtcSX', 'name':'hubSOL', 'id':'117'},
        {'key':'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn', 'name':'JitoSOL', 'id':'118'},
        {'key':'7Q2afV64in6N6SeZsAAB81TJzwDoD6zpqmHkzi9Dcavn', 'name':'JSOL', 'id':'119'},
        {'key':'jucy5XJ76pHVvtPZb5TKRcGQExkwit2P5s4vY8UzmpC', 'name':'jucySOL', 'id':'120'},
        {'key':'jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v', 'name':'JupSOL', 'id':'121'},
        {'key':'LAinEtNLgpmCP9Rvsf5Hn8W6EhNiKLZQti1xfWMLy6X', 'name':'laineSOL', 'id':'122'},
        {'key':'LnTRntk2kTfWEY6cVB8K9649pgJbt6dJLS1Ns1GZCWg', 'name':'lanternSOL', 'id':'123'},
        {'key':'LSTxxxnJzKDFSLr4dUkPcmCf5VyryEqzPLz5j4bpxFp', 'name':'LST', 'id':'124'},
        {'key':'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So', 'name':'mSOL', 'id':'125'},
        {'key':'pathdXw4He1Xk3eX84pDdDZnGKEme3GivBamGCVPZ5a', 'name':'pathSOL', 'id':'126'},
        {'key':'phaseZSfPxTDBpiVb96H4XFSD8xHeHxZre5HerehBJG', 'name':'phaseSOL', 'id':'127'},
        {'key':'picobAEvs6w7QEknPce34wAE4gknZA9v5tTonnmHYdX', 'name':'picoSOL', 'id':'128'},
        {'key':'pumpkinsEq8xENVZE6QgTS93EN4r9iKvNxNALS1ooyp', 'name':'pumpkinSOL', 'id':'129'},
        {'key':'pWrSoLAhue6jUxUkbWgmEy5rD9VJzkFmvfTDV5KgNuu', 'name':'pwrSOL', 'id':'130'},
        {'key':'st8QujHLPsX3d6HG9uQg9kJ91jFxUgruwsb1hyYXSNd', 'name':'stakeSOL', 'id':'131'},
        {'key':'strng7mqqc1MBJJV6vMzYbEqnwVGvKKGKedeCvtktWA', 'name':'strongSOL', 'id':'132'},
        {'key':'suPer8CPwxoJPQ7zksGMwFvjBQhjAHwUMmPV4FVatBw', 'name':'superSOL', 'id':'133'},
        {'key':'Zippybh3S5xYYam2nvL6hVJKz1got6ShgV4DyD1XQYF', 'name':'zippySOL', 'id':'134'},
        ]
    api_url = 'https://sanctum-extra-api.ngrok.dev/v1/apy/latest?lst=fpSoL8EJ7UA5yJxFKWk1MFiWi35w8CbH36G5B9d7DsV&lst=Fi5GayacZzUrfaCRCJtBz2vSYkGF56xjgCceZx5SbXwq&lst=pathdXw4He1Xk3eX84pDdDZnGKEme3GivBamGCVPZ5a&lst=jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v&lst=BgYgFYq4A9a2o5S1QbWkmYVFBh7LBQL8YvugdhieFg38&lst=phaseZSfPxTDBpiVb96H4XFSD8xHeHxZre5HerehBJG&lst=BANXyWgPpa519e2MtQF1ecRbKYKKDMXPF1dyBxUq9NQG&lst=iceSdwqztAQFuH6En49HWwMxwthKMnGzLFQcMN3Bqhj&lst=pWrSoLAhue6jUxUkbWgmEy5rD9VJzkFmvfTDV5KgNuu&lst=suPer8CPwxoJPQ7zksGMwFvjBQhjAHwUMmPV4FVatBw&lst=jucy5XJ76pHVvtPZb5TKRcGQExkwit2P5s4vY8UzmpC&lst=BonK1YhkXEGLZzwtcvRTip3gAL9nCeQD7ppZBLXhtTs&lst=Dso1bDeDjCQxTrWHqUUi63oBvV7Mdm6WaobLbQ7gnPQ&lst=Comp4ssDzXcLeu2MnLuGNNFC4cmLPMng8qWHPvzAMU1h&lst=picobAEvs6w7QEknPce34wAE4gknZA9v5tTonnmHYdX&lst=GRJQtWwdJmp5LLpy8JWjPgn5FnLyqSJGNhn5ZnCTFUwM&lst=HUBsveNpjo5pWqNkH57QzxjQASdTVXcSK7bVKTSZtcSX&lst=strng7mqqc1MBJJV6vMzYbEqnwVGvKKGKedeCvtktWA&lst=LnTRntk2kTfWEY6cVB8K9649pgJbt6dJLS1Ns1GZCWg&lst=st8QujHLPsX3d6HG9uQg9kJ91jFxUgruwsb1hyYXSNd&lst=pumpkinsEq8xENVZE6QgTS93EN4r9iKvNxNALS1ooyp&lst=he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A&lst=CgnTSoL3DgY9SFHxcLj6CgCgKKoTBr6tp4CPAEWy25DE&lst=LAinEtNLgpmCP9Rvsf5Hn8W6EhNiKLZQti1xfWMLy6X&lst=vSoLxydx6akxyMD9XEcPvGYNGq6Nn66oqVb3UkGkei7&lst=bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1&lst=GEJpt3Wjmr628FqXxTgxMce1pLntcPV4uFi8ksxMyPQh&lst=J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn&lst=7Q2afV64in6N6SeZsAAB81TJzwDoD6zpqmHkzi9Dcavn&lst=LSTxxxnJzKDFSLr4dUkPcmCf5VyryEqzPLz5j4bpxFp&lst=Zippybh3S5xYYam2nvL6hVJKz1got6ShgV4DyD1XQYF&lst=edge86g9cVz87xcpKpy3J77vbp4wYd9idEV562CCntt&lst=ThUGsoLWtoTCfb24AmQTKDVjTTUBbNrUrozupJeyPsy&lst=WensoLXxZJnev2YvihHFchn1dVVFnFLYvgomXWvvwRu&lst=5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm&lst=7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj&lst=mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So'
    api_data = call_api(api_url)
    print_data(api_data)

if __name__ == "__main__":
    sanctum()