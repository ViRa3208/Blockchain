from __future__ import annotations

import argparse
import sys
import requests
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import PrivateKey, P2wpkhAddress
from bitcoinutils.script import Script

# Конфигурация
WIF = "cPBNEHScJZE8oxu3SFfuJjwkSSWeaMxLPKiSiuadjviSrAcgKPAb"
FROM_ADDRESS = "tb1qkesll0fxu6h2x3070pvd604mx4yt234nytlw8w"
MEMPOOL_URL = "https://mempool.space/testnet4/api"


def main():
    parser = argparse.ArgumentParser(description="Отправить биткоины")
    parser.add_argument("--to", required=True, help="Адрес получателя")
    args = parser.parse_args()

    # Фиксированная сумма для отправки: 0.00336655 BTC = 336655 сатоши
    send_amount = 750

    # Инициализация сети
    setup("testnet")

    # Получаем все UTXO отправителя
    url = f"{MEMPOOL_URL}/address/{FROM_ADDRESS}/utxo"
    utxos = requests.get(url).json()

    if not utxos:
        print("Нет средств на кошельке")
        return

    # Вычисляем общий баланс
    total_balance = sum(int(utxo["value"]) for utxo in utxos)
    print(f"Общий баланс: {total_balance} сатоши ({total_balance / 100000000:.8f} BTC)")
    print(f"Пытаюсь отправить: {send_amount} сатоши ({send_amount / 100000000:.8f} BTC)")

    # Рассчитываем комиссию (примерно 250 сатоши для надежности)
    fee = 250
    total_needed = send_amount + fee

    if total_needed > total_balance:
        print(f"Недостаточно средств. Нужно: {total_needed} сатоши, есть: {total_balance} сатоши")
        return

    # Подбираем UTXO для отправки
    selected_utxos = []
    selected_total = 0

    # Сортируем UTXO по величине (от больших к меньшим)
    sorted_utxos = sorted(utxos, key=lambda x: int(x["value"]), reverse=True)

    for utxo in sorted_utxos:
        if selected_total >= total_needed:
            break
        selected_utxos.append(utxo)
        selected_total += int(utxo["value"])

    print(f"Выбрано {len(selected_utxos)} UTXO на сумму {selected_total} сатоши")

    # Рассчитываем сдачу
    change = selected_total - send_amount - fee

    # Создаем приватный ключ
    priv = PrivateKey(WIF)
    pub = priv.get_public_key()

    # Создаем адрес получателя
    to_address = P2wpkhAddress(args.to)

    # Создаем входы транзакции
    tx_inputs = []
    for utxo in selected_utxos:
        txin = TxInput(utxo["txid"], int(utxo["vout"]))
        tx_inputs.append(txin)

    # Создаем выходы транзакции
    outputs = [TxOutput(send_amount, to_address.to_script_pub_key())]

    # Добавляем сдачу, если она больше 0
    if change > 0:
        from_address_obj = P2wpkhAddress(FROM_ADDRESS)
        outputs.append(TxOutput(change, from_address_obj.to_script_pub_key()))
        print(f"Сдача: {change} сатоши ({change / 100000000:.8f} BTC)")

    # Создаем транзакцию
    tx = Transaction(tx_inputs, outputs, has_segwit=True)

    # Подготавливаем scriptCode для подписи
    h160 = pub.to_hash160()
    script_code = Script(["OP_DUP", "OP_HASH160", h160, "OP_EQUALVERIFY", "OP_CHECKSIG"])

    # Подписываем каждый вход
    tx.witnesses = []
    for idx, utxo in enumerate(selected_utxos):
        sig = priv.sign_segwit_input(tx, idx, script_code, int(utxo["value"]))
        tx.witnesses.append(TxWitnessInput([sig, pub.to_hex()]))
        print(f"Подписан вход {idx + 1}: {utxo['txid'][:20]}...:{utxo['vout']}")

    # Получаем raw транзакцию
    raw_tx = tx.serialize()
    txid = tx.get_txid()

    # Отправляем транзакцию
    print("\nОтправляю транзакцию в сеть...")
    broadcast_url = f"{MEMPOOL_URL}/tx"
    response = requests.post(broadcast_url, data=raw_tx.encode('utf-8'))

    if response.status_code == 200:
        print("\n" + "=" * 50)
        print("ТРАНЗАКЦИЯ УСПЕШНО ОТПРАВЛЕНА!")
        print("=" * 50)
        print(f"TXID: {txid}")
        print(f"Сумма отправки: {send_amount} сатоши ({send_amount / 100000000:.8f} BTC)")
        print(f"Адрес получателя: {args.to}")
        print(f"Комиссия: {fee} сатоши")
        print(f"Количество входов: {len(selected_utxos)}")
        if change > 0:
            print(f"Сдача возвращена: {change} сатоши ({change / 100000000:.8f} BTC)")

        print(f"\nСсылка для просмотра:")
        print(f"https://mempool.space/testnet4/tx/{txid}")
        print("=" * 50)
    else:
        print(f"\nОШИБКА при отправке транзакции:")
        print(f"Код ошибки: {response.status_code}")
        print(f"Ответ: {response.text}")
        print(f"\nRaw транзакция (для ручной отправки):")
        print(raw_tx)


if __name__ == "__main__":
    main()