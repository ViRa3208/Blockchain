import requests
import json

def get_bitcoin_balance(address):
    try:
        # Определяем сеть по префиксу адреса
        if address.startswith(('tb1', '2', 'n', 'm')):  # Testnet адреса
            base_url = "https://mempool.space/testnet/api"
            network = "testnet"
        else:  # Mainnet адреса
            base_url = "https://mempool.space/api"
            network = "mainnet"

        print(f"Using {network} API...")

        url = f"{base_url}/address/{address}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        balance_satoshis = data["chain_stats"]["funded_txo_sum"] - data["chain_stats"]["spent_txo_sum"]

        # Создаем информацию о балансе
        balance_info = {
            "address": address,
            "network": network,
            "balance_satoshis": balance_satoshis,
            "balance_btc": balance_satoshis / 100000000,
            "total_received": data["chain_stats"]["funded_txo_sum"],
            "total_sent": data["chain_stats"]["spent_txo_sum"],
            "transaction_count": data["chain_stats"]["tx_count"]
        }

        # Сохраняем в JSON файл
        filename = f"bitcoin_balance_{address}.json"
        with open(filename, 'w') as f:
            json.dump(balance_info, f, indent=2)

        return balance_info, filename

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch data - {e}")
        return None, None
    except KeyError as e:
        print(f"Error: Unexpected API response format - {e}")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def main():
    # Получаем Bitcoin адрес от пользователя
    address = input("Enter Bitcoin address: ").strip()

    if not address:
        print("Error: No address provided!")
        return

    print(f"Fetching balance for: {address}")

    # Получаем баланс и сохраняем в JSON
    balance_data, filename = get_bitcoin_balance(address)

    if balance_data and filename:
        print(f"\nBalance information saved to: {filename}")
        print(f"Network: {balance_data['network']}")
        print(f"Balance: {balance_data['balance_btc']:.8f} BTC")
        print(f"Satoshis: {balance_data['balance_satoshis']:,}")
        print(f"Total Received: {balance_data['total_received']:,} satoshis")
        print(f"Total Sent: {balance_data['total_sent']:,} satoshis")
        print(f"Transactions: {balance_data['transaction_count']}")
    else:
        print("Failed to get balance information")

if __name__ == "__main__":
    main()