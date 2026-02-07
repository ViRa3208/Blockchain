# electrum_export.py
import json
import sys
from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey


def main():
    # Экспортируйте приватные ключи из Electrum:
    # 1. Откройте Electrum
    # 2. Wallet → Private keys → Export
    # 3. Сохраните в JSON

    setup("testnet")

    # Пример JSON структуры Electrum
    electrum_data = {

            "tb1qkesll0fxu6h2x3070pvd604mx4yt234nytlw8w": "p2wpkh:cPBNEHScJZE8oxu3SFfuJjwkSSWeaMxLPKiSiuadjviSrAcgKPAb",
            "tb1qctxjw8xekeyfz4t27zvmr366zfc63yfy8l85uh": "p2wpkh:cV2gBswkhUd1Uz29BYSHqgMLYLxn1YGJqeLTxzN1b2yHej1JyXJx",
            "tb1q7kxtaj5kq8e7thfwaqza34946zc8fwxe2py2r7": "p2wpkh:cUCvSiCKuc7bnYzBhj9xEfVG2KWt76HReEjPmUkFfoaJKsAZhL2J",
            "tb1q0spnw6st8v9warp4fgk2erp9sewzh0geuzxf5a": "p2wpkh:cSFe782wXEjCTPoUW3vQgxcrQrMPSwjnGSpyfjpFrncFCYnedFK7",
            "tb1q28wvsmpvh7km5yamsculcj59cn230nptxjlsam": "p2wpkh:cSUVVp8HkWhLWaYikb2yuHo2XyCVA9XEiHv5XNvzs9a6YaFkntYS",
            "tb1qwmgx5nu5l29j8x6hlx7ah6eqqjzr5lxf70gep8": "p2wpkh:cMteip6FKrtjP6DhSz1Hc9GUhPZhABEwfd4sqpkAZ3FQXDqnJTrt",
            "tb1q3gc2y5f9t7qv5judzlwtkhh8zujqhjm8p25ysg": "p2wpkh:cNXhCtbRe7tgnFtoK58RupfE3tyoQwv7CJNBNJ59Up22PEtuMbod",
            "tb1q4sjc4e7f9vma9mqvfs7yclwtlh4muk0ajffqju": "p2wpkh:cP4jNqj1sAnHNgHejwuMjbijit4ZCfPVxQhiYTnn5sg7Gz4o4WEQ",
            "tb1qtdyh8rdxg2us3jku85xrj0uwzycczcgam72sc5": "p2wpkh:cV35qKuzeFiiTWJY7DXbdpuBQveSXyzQUbcg6qVZmmnwmUpcnxkm",
            "tb1qfsy824k93dyd6rf7weqku9jc8dtkefmp9xzgcn": "p2wpkh:cVncQY7Pfj5cQ3KKYky4adpiRbHLEHo17fnbavwVbskkRR9MPYVC",
            "tb1qfhzfjfufg5kjdlrn3fnclj30fgf4lgg6dylwjs": "p2wpkh:cTQRtgyrZTzMKqD3krbNaWHhwcPsUntZFfaH1cbF4UTbLUkWEV8g",
            "tb1qy7dmq638p5veg49mehvtewgw4wzwjwe0l6ftu6": "p2wpkh:cQhCfTELfYvbyCgKSY8hBrcKVaiej1RDP67btkNAuB5z5nYTcK5T",
            "tb1qegrt20ckr23tguhwgq990ndr7vxtrlgu88v7dc": "p2wpkh:cNUCrJm13BgGCipSU7xMo41vR35L8HgpDibgagsKTbZ23MSNDYEY",
            "tb1q66jptlh8x9s6sx68f5jsfch0w90wfaqzfw9sz4": "p2wpkh:cQ37W3z8yfNqfBahCnTZnaMDedFjXJ9PeQ4RmEeMJmyAdQLfwGFt",
            "tb1q7y78w2ele6kzg0u5mwrrg8wlt86ur79x079p97": "p2wpkh:cW4ZHFciyyAuoaXTFeXcnSEk5s1ENBG7Phm8xAjeMhxS1gnCd5RQ",
            "tb1qvn8z7ms6rzlv8ghywtcre76n7kty2qylcvfwl3": "p2wpkh:cQV8Njb2DQLPErcCiz13GLqB5hBerg1qNrVX23wEKQzue7vuUEHK",
            "tb1qm63rhctxjpj5gygj8xprcnggqytet48m58r3yz": "p2wpkh:cRwtG2RShmt3aczDcQq97TA5MVtG2fCV4hiGVungG1MvBEWo8361",
            "tb1q2t56l39qac05cqrkp7pza60t0cttffchh4k3ql": "p2wpkh:cNWS9PkoQkBcKVQfD3HABwJv2bXPSmxkqBZLu3fGRr78dUr4J5cq",
            "tb1qr0805yn8kt7kp0cs6d7k3t0hn249lemu08umt3": "p2wpkh:cUZ1M7pHEA4SYpLXM21c8RtxhFpQw3Z4xnY8aL25GQDz5B5iLf8i",
            "tb1qgqex26lju7tpwlzkfd5mk6wuqaempxqeyjhac6": "p2wpkh:cVc9kQmonYaasPXWbM9x3cJ94exLJqssqANsJhp8pJ52ewswxqiR",
            "tb1qrmzd39lhe4np4hdlyhtr5sfwurvhvacgz2nkgh": "p2wpkh:cSmfg4MeTDeEGLTzkZovLzLHtTbXuhr1qDx8sWJeEEd8dY1EbGTU",
            "tb1qdcmhsjzekh75w3hjlkrgwms64fzwyyte9lthg4": "p2wpkh:cRFoSkCiL1iEubRAFKMVnwawoKJE3EwspYd79FjNcm5dP5P1t7Cf",
            "tb1q7gzlczfrzxn9aw8a4u68psfgwjdrph0896wd7w": "p2wpkh:cMbtCM4SdsrSpPgpe2P55NsvujqjoxCDPL4YQnBwof2kqAameYnL",
            "tb1qrw90u3ja4k86myw7e2v8fn0zrzrq0c9wp6a6qs": "p2wpkh:cUeVmweTYWwXdVgSc1S3WDqzZPMfSEogFyDSFF6GRJwCtTdYkymz",
            "tb1qdkqd9t492svpe6pp2h0stdyryaj580m42u6k3w": "p2wpkh:cRxLrJhKajv7YuVZUfH9KQhcxAK57JVBz3ZPtJBQrDut2erQ51Y6",
            "tb1qq5ldzxmxp9numan5jv3zhllpngumz8n4fue4g7": "p2wpkh:cPPrrNXu6LhWr8L8d1VCKu8pGtybrHHeuR5qopvhLmEJaKsdfsFK",
            "tb1q3sag67lp69kmuu9t25gzpszf4xtvy6j62s9kjh": "p2wpkh:cMyppFFqZPK7ThWkPLhuhqVKtHQ6Fd5D8KHwhQPVXxKpa4uyHwEW",
            "tb1qfh39jps5vux24qeuad9zd4jp3dj4pfwk69e63p": "p2wpkh:cRrZZf11CzvYeALGnMhzTWAe82RE12qMruMKTskdv3wNAo6NnEBt",
            "tb1q3v0klz8aeqfnv6wegvu6unehhkpl0nsmur65jv": "p2wpkh:cPbUTr4EkTZJSAwrxoMGDjopSqbTyrN7JRbme9GNjQabRxKPTkdy",
            "tb1qk500g75xvnvw5sv6zkf5e7a90wtn2yxcv59z5h": "p2wpkh:cPJK81u1v5XxLwvuh8JMFmphTZTVVzG6cMuWr25ckJ9EqjCkn4yV",
            "tb1q0eqx9ldw8n4wrz5zngp0k40jj7t0ucsxlksuew": "p2wpkh:cTpqcQWExRzknLhibPhCreJeQYmv91v7AUq6ixLtXfpbiX3n9nfQ"

    }

    target_addr = input("Enter your tb1q address: ").strip().lower()

    for addr, wif in electrum_data.items():
        if addr.lower() == target_addr:
            # Убираем префикс типа
            if ":" in wif:
                wif = wif.split(":")[1]

            print(f"Found!")
            print(f"Address: {addr}")
            print(f"WIF: {wif}")

            # Проверяем
            priv = PrivateKey(wif)
            derived_addr = priv.get_public_key().get_segwit_address().to_string()

            if derived_addr.lower() == target_addr:
                print("✓ WIF matches address")
            else:
                print("✗ WIF doesn't match")
            return

    print("Address not found in exported keys")


if __name__ == "__main__":
    main()