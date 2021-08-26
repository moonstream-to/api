import argparse
import base64
import json
from pprint import pprint
import string
import time
from typing import Any, Collection, Dict

from moonstreamdb.models import EthereumAddress, EthereumLabel
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import label, text
import requests

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}


def make_request(headers: Dict[str, Any], data: Dict[str, Any]):
    time.sleep(3)

    try:

        while True:

            grapql_resp = session.get(
                "https://api.opensea.io/graphql/",
                headers=headers,
                json=data,
            )

            if "Too many requests" in grapql_resp.text:
                time.sleep(3)
            else:
                break

        # Too many requests. Please wait 180559 microseconds.
        # print(grapql_resp.text)
        json_response = grapql_resp.json()
    except Exception as err:
        print(err)
        print(grapql_resp.text)

    return json_response


def check_if_third_requred(query: str, data: Dict[str, Any]):

    required = False

    message = str(f"arrayconnection:{9900}")
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)

    data["variables"]["cursor"] = base64_bytes.decode("utf-8")

    data["variables"]["query"] = query

    response_result = make_request(headers=headers, data=data)

    try:
        print(len(response_result["data"]["query"]["collections"]["edges"]))
        pprint(response_result["data"]["query"]["collections"]["edges"][0])
        required = True
    except TypeError:
        pass
    except IndexError:
        pass
    except Exception as err:
        print(err)
        raise
    return required


def write_contract_to_database(
    db_session: Session,
    token_address: str,
    blockchain: str,
    name: str,
    slug: str,
    image_url: str,
):

    # Writing labels to db

    """
    db_session=db_session,
    token_address=contract_address,
    blockchain=blockchain,
    name=name,
    slug=slug,
    image_url=image_url

    """
    address_id = (
        db_session.query(EthereumAddress.id)
        .filter(EthereumAddress.address == token_address)
        .one_or_none()
    )

    if not address_id:
        try:
            print("Adding address")
            register_address = EthereumAddress(address=token_address)
            db_session.add(register_address)
            db_session.commit()
            address_id = register_address.id
        except Exception as err:

            db_session.rollback()
            print(err)
    else:
        address_id = address_id[0]

    # db_session.query(EthereumAddress.id).order_by(text("id desc")).limit(1).one()

    label_data = (
        {
            "name": name,
            "opensea_url": f"https://etherscan.io/assets/{slug}",
            "blockchain": blockchain,
            "imageUrl": image_url,
        },
    )

    eth_label = EthereumLabel(
        label="opensea_nft",
        address_id=address_id,
        label_data=label_data,
    )
    try:
        print("Adding label")
        db_session.add(eth_label)
        db_session.commit()
    except Exception as err:
        print(f"Failed adding {token_address} label to db err:{err}")
        db_session.rollback()


def parse_contract(db_session: Session, collection: Dict[str, Any]):
    """
    Crawl from collection endpoint
    """

    # collection_type = collection["nodes"]

    # collection_payload = {
    #     "id": "collectionQuery",
    #     "query": "query collectionQuery(\n  $collection: CollectionSlug!\n  $collections: [CollectionSlug!]\n  $collectionQuery: String\n  $includeHiddenCollections: Boolean\n  $numericTraits: [TraitRangeType!]\n  $query: String\n  $sortAscending: Boolean\n  $sortBy: SearchSortBy\n  $stringTraits: [TraitInputType!]\n  $toggles: [SearchToggle!]\n  $showContextMenu: Boolean\n) {\n  collection(collection: $collection) {\n    isEditable\n    bannerImageUrl\n    name\n    description\n    imageUrl\n    relayId\n    representativeAsset {\n      assetContract {\n        openseaVersion\n        id\n      }\n      id\n    }\n    ...collection_url\n    ...CollectionHeader_data\n    id\n  }\n  assets: query {\n    ...AssetSearch_data_1bS60n\n  }\n}\n\nfragment AssetCardContent_asset on AssetType {\n  relayId\n  name\n  ...AssetMedia_asset\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n  isDelisted\n}\n\nfragment AssetCardContent_assetBundle on AssetBundleType {\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          relayId\n          ...AssetMedia_asset\n          id\n        }\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_assetBundle on AssetBundleType {\n  name\n  assetCount\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          collection {\n            name\n            relayId\n            isVerified\n            id\n          }\n          id\n        }\n        id\n      }\n    }\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_asset_2V84VL on AssetType {\n  name\n  tokenId\n  collection {\n    name\n    isVerified\n    id\n  }\n  hasUnlockableContent\n  isDelisted\n  isFrozen\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  assetEventData {\n    firstTransfer {\n      timestamp\n    }\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  decimals\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardHeader_data_27d9G3 on AssetType {\n  relayId\n  favoritesCount\n  isDelisted\n  isFavorite\n  ...AssetContextMenu_data_3z4lq0 @include(if: $showContextMenu)\n}\n\nfragment AssetContextMenu_data_3z4lq0 on AssetType {\n  ...asset_edit_url\n  ...itemEvents_data\n  isDelisted\n  isEditable {\n    value\n    reason\n  }\n  isListable\n  ownership(identity: {}) {\n    isPrivate\n    quantity\n  }\n  creator {\n    address\n    id\n  }\n  collection {\n    isAuthorizedEditor\n    id\n  }\n}\n\nfragment AssetMedia_asset on AssetType {\n  animationUrl\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n  isDelisted\n  displayImageUrl\n}\n\nfragment AssetQuantity_data on AssetQuantityType {\n  asset {\n    ...Price_data\n    id\n  }\n  quantity\n}\n\nfragment AssetSearchFilter_data_1GloFv on Query {\n  ...CollectionFilter_data_tXjHb\n  collection(collection: $collection) {\n    numericTraits {\n      key\n      value {\n        max\n        min\n      }\n      ...NumericTraitFilter_data\n    }\n    stringTraits {\n      key\n      ...StringTraitFilter_data\n    }\n    id\n  }\n  ...PaymentFilter_data_2YoIWt\n}\n\nfragment AssetSearchList_data_gVyhu on SearchResultType {\n  asset {\n    assetContract {\n      address\n      chain\n      id\n    }\n    collection {\n      isVerified\n      id\n    }\n    relayId\n    tokenId\n    ...AssetSelectionItem_data\n    ...asset_url\n    id\n  }\n  assetBundle {\n    relayId\n    id\n  }\n  ...Asset_data_gVyhu\n}\n\nfragment AssetSearch_data_1bS60n on Query {\n  ...CollectionHeadMetadata_data_2YoIWt\n  ...AssetSearchFilter_data_1GloFv\n  ...SearchPills_data_2Kg4Sq\n  search(collections: $collections, first: 2000, numericTraits: $numericTraits, querystring: $query, resultType: ASSETS, sortAscending: $sortAscending, sortBy: $sortBy, stringTraits: $stringTraits, toggles: $toggles) {\n    edges {\n      node {\n        ...AssetSearchList_data_gVyhu\n        __typename\n      }\n      cursor\n    }\n    totalCount\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment AssetSelectionItem_data on AssetType {\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    imageUrl\n    id\n  }\n  imageUrl\n  name\n  relayId\n}\n\nfragment Asset_data_gVyhu on SearchResultType {\n  asset {\n    isDelisted\n    ...AssetCardHeader_data_27d9G3\n    ...AssetCardContent_asset\n    ...AssetCardFooter_asset_2V84VL\n    ...AssetMedia_asset\n    ...asset_url\n    ...itemEvents_data\n    id\n  }\n  assetBundle {\n    ...bundle_url\n    ...AssetCardContent_assetBundle\n    ...AssetCardFooter_assetBundle\n    id\n  }\n}\n\nfragment CollectionFilter_data_tXjHb on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(first: 100, includeHidden: $includeHiddenCollections, query: $collectionQuery, sortBy: SEVEN_DAY_VOLUME) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment CollectionHeadMetadata_data_2YoIWt on Query {\n  collection(collection: $collection) {\n    bannerImageUrl\n    description\n    imageUrl\n    name\n    id\n  }\n}\n\nfragment CollectionHeader_data on CollectionType {\n  name\n  description\n  imageUrl\n  bannerImageUrl\n  ...CollectionStatsBar_data\n  ...SocialBar_data\n  ...verification_data\n}\n\nfragment CollectionModalContent_data on CollectionType {\n  description\n  imageUrl\n  name\n  slug\n}\n\nfragment CollectionStatsBar_data on CollectionType {\n  stats {\n    numOwners\n    totalSupply\n    totalVolume\n    floorPrice\n    id\n  }\n  slug\n}\n\nfragment NumericTraitFilter_data on NumericTraitTypePair {\n  key\n  value {\n    max\n    min\n  }\n}\n\nfragment PaymentFilter_data_2YoIWt on Query {\n  paymentAssets(first: 10) {\n    edges {\n      node {\n        symbol\n        relayId\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n  PaymentFilter_collection: collection(collection: $collection) {\n    paymentAssets {\n      symbol\n      relayId\n      id\n    }\n    id\n  }\n}\n\nfragment Price_data on AssetType {\n  decimals\n  imageUrl\n  symbol\n  usdSpotPrice\n  assetContract {\n    blockExplorerLink\n    chain\n    id\n  }\n}\n\nfragment SearchPills_data_2Kg4Sq on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        imageUrl\n        name\n        slug\n        ...CollectionModalContent_data\n        id\n      }\n    }\n  }\n}\n\nfragment SocialBar_data on CollectionType {\n  discordUrl\n  externalUrl\n  instagramUsername\n  mediumUsername\n  slug\n  telegramUrl\n  twitterUsername\n  ...collection_url\n}\n\nfragment StringTraitFilter_data on StringTraitType {\n  counts {\n    count\n    value\n  }\n  key\n}\n\nfragment asset_edit_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n}\n\nfragment asset_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment bundle_url on AssetBundleType {\n  slug\n}\n\nfragment collection_url on CollectionType {\n  slug\n}\n\nfragment itemEvents_data on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment verification_data on CollectionType {\n  isMintable\n  isSafelisted\n  isVerified\n}\n",
    #     "variables": {
    #         "collectionQuery": None,
    #         "collections": [collection_type["slug"]],
    #         "includeHiddenCollections": None,
    #         "numericTraits": None,
    #         "query": None,
    #         "showContextMenu": True,
    #         "sortAscending": True,
    #         "sortBy": "PRICE",
    #         "stringTraits": None,
    #         "toggles": None,
    #     },
    # }

    # results = make_request(headers=headers, data=collection_payload)

    try:
        name = collection["node"]["name"]
        slug = collection["node"]["slug"]
        contract_address = collection["node"]["representativeAsset"]["assetContract"][
            "address"
        ]
        blockchain = collection["node"]["representativeAsset"]["assetContract"]["chain"]
        image_url = collection["node"]["imageUrl"]
        write_contract_to_database(
            db_session=db_session,
            token_address=contract_address,
            blockchain=blockchain,
            name=name,
            slug=slug,
            image_url=image_url,
        )
    except:
        print("empty collection")


def crawl_collections_query_loop(
    db_session: Session,
    query: str,
    start_cursour: int,
    index: int,
    payload: Dict[str, Any],
):
    while True:
        message = str(f"arrayconnection:{start_cursour}")
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        print(start_cursour)

        payload["variables"]["cursor"] = base64_bytes.decode("utf-8")

        payload["variables"]["query"] = query

        json_response = make_request(headers=headers, data=payload)
        # print(base64_bytes.decode("utf-8"))
        try:
            start_cursour += len(json_response["data"]["query"]["collections"]["edges"])
            pprint(json_response["data"]["query"]["collections"]["edges"][0])
        except TypeError:
            break
        except IndexError:
            break
        except Exception as err:
            raise

        pprint(json_response["data"]["query"]["collections"]["edges"][0])
        print(json_response["data"]["query"].keys())
        print(query)
        print(
            base64.b64decode(
                json_response["data"]["query"]["collections"]["edges"][-1]["cursor"]
            )
        )

        for collection_types_oblect in json_response["data"]["query"]["collections"][
            "edges"
        ]:
            pprint(collection_types_oblect)
            print(
                collection_types_oblect["node"]["slug"],
                collection_types_oblect["node"]["representativeAsset"],
            )
            if collection_types_oblect["node"]["representativeAsset"]:
                parse_contract(
                    db_session=db_session, collection=collection_types_oblect
                )

        with open(f"data/page_{query}_{index}.json", "w") as output:
            # output.write(grapql_resp.text)
            json.dump(json_response, output)
        index += 1


def crawl_opensea(args: argparse.Namespace):
    BASE_TOKEN_URL = "https://opensea.io/assets"

    # session = requests.Session()

    page = session.get(BASE_TOKEN_URL, headers=headers)
    print()
    print(page.status_code)

    with yield_db_session_ctx() as db_session:
        grapql_collections_payload = {
            "id": "CollectionFilterQuery",
            "query": "query CollectionFilterQuery(\n  $assetOwner: IdentityInputType\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $includeHidden: Boolean\n  $query: String\n  $sortBy: CollectionSort\n) {\n  query {\n    ...CollectionFilter_data_421KmG\n  }\n}\n\nfragment CollectionFilter_data_421KmG on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n   stats {\n totalSupply\n }\n      TotalCount\n   representativeAsset {\n      assetContract {\n  name\n label\n  address\n     openseaVersion\n        id\n      }\n      id\n    }\n     imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(after: $cursor, assetOwner: $assetOwner, chains: $chains, first: $count, includeHidden: $includeHidden, parents: $categories, query: $query, sortBy: $sortBy) {\n    edges {\n      node {\n  author {\n address\n  id\n  }\n   TotalCount\n   representativeAsset {\n      assetContract {\n   address\n  chain\n   openseaVersion\n        id\n      }\n      id\n    }\n   assetCount\n  stats {\n totalSupply\n }\n      imageUrl\n        name\n        slug\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n",
            "variables": {
                "assetOwner": None,
                "categories": None,
                "chains": None,
                "collections": [],
                "count": 100,
                "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                "includeHidden": False,
                "query": None,
                "sortBy": "CREATED_DATE",
            },
        }
        alphabet_string = string.ascii_lowercase

        for first_letter in alphabet_string:

            for second_letter in alphabet_string:
                search_query = first_letter + second_letter

                third_required = check_if_third_requred(
                    search_query, grapql_collections_payload
                )

                print(third_required)

                if third_required:
                    for third_letter in alphabet_string:
                        search_query = search_query + third_letter
                        crawl_collections_query_loop(
                            db_session, search_query, 0, 1, grapql_collections_payload
                        )
                else:
                    crawl_collections_query_loop(
                        db_session, search_query, 0, 1, grapql_collections_payload
                    )


def main():
    parser = argparse.ArgumentParser(
        description="Crawls smart contract sources from etherscan.io"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    crawl_parser = subcommands.add_parser(
        "crawl", description="Crawling data from source"
    )
    crawl_parser.set_defaults(func=lambda _: crawl_parser.print_help())
    subcommnds_crawl = crawl_parser.add_subparsers(
        description="Crawl rcontracts commands"
    )

    nft_parser = subcommnds_crawl.add_parser("nfts", description="Get nfts contracts")
    nft_parser.set_defaults(func=lambda _: nft_parser.print_help())
    nft_parser.set_defaults(func=crawl_opensea)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


# collection load
# grapql_collections_payload = {
#     "id": "CollectionFilterQuery",
#     "query": str(
#         (
#             "query CollectionFilterQuery(\n  $assetOwner: IdentityInputType\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $includeHidden: Boolean\n  $query: String\n  $sortBy: CollectionSort\n) {\n  query {\n    ...CollectionFilter_data_421KmG\n  }\n}\n\nfragment CollectionFilter_data_421KmG on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(after: $cursor, assetOwner: $assetOwner, chains: $chains, first: $count, includeHidden: $includeHidden, parents: $categories, query: $query, sortBy: $sortBy)"
#             + "{\n    edges {\n      node {\n "
#             + "   imageUrl\n    "
#             + "    name\n   "
#             + "     slug\n    "
#             + "    id\n   "
#             + "     __typename\n      }\n  "
#             + "    cursor\n    }\n  "
#             + "  pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n "
#         )
#     ),
#     "variables": {
#         "assetOwner": None,
#         "categories": None,
#         "chains": None,
#         "collections": [],
#         "count": 100,
#         "cursor": "YXJyYXljb25uZWN0aW9uOjI5OQ==",
#         "includeHidden": False,
#         "query": None,
#         "sortBy": "SEVEN_DAY_VOLUME",
#     },
# }

# Collection CollectionsScrollerQuery

# collection


# collection load
# grapql_collections_payload = {
#     "id": "CollectionFilterQuery",
#     "query": str(
#         (
#             "query CollectionFilterQuery(\n  $assetOwner: IdentityInputType\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $includeHidden: Boolean\n  $query: String\n  $sortBy: CollectionSort\n) {\n  query {\n    ...CollectionFilter_data_421KmG\n  }\n}\n\nfragment CollectionFilter_data_421KmG on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(after: $cursor, assetOwner: $assetOwner, chains: $chains, first: $count, includeHidden: $includeHidden, parents: $categories, query: $query, sortBy: $sortBy)"
#             + "{\n    edges {\n      node {\n "
#             + "   imageUrl\n    "
#             + "    name\n   "
#             + "     slug\n    "
#             + "    id\n   "
#             + "     __typename\n      }\n  "
#             + "    cursor\n    }\n  "
#             + "  pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n "
#         )
#     ),
#     "variables": {
#         "assetOwner": None,
#         "categories": None,
#         "chains": None,
#         "collections": [],
#         "count": 100,
#         "cursor": "YXJyYXljb25uZWN0aW9uOjI5OQ==",
#         "includeHidden": False,
#         "query": None,
#         "sortBy": "SEVEN_DAY_VOLUME",
#     },
# }

# Collection CollectionsScrollerQuery

# collection


# generate dict view

# assets query
# grapql_assests_payload = {
#     "id": "AssetSearchQuery",
#     "query": "query AssetSearchQuery(\n  $categories: [CollectionSlug!]\n  $chains: [ChainScalar!]\n  $collection: CollectionSlug\n  $collectionQuery: String\n  $collectionSortBy: CollectionSort\n  $collections: [CollectionSlug!]\n  $count: Int\n  $cursor: String\n  $identity: IdentityInputType\n  $includeHiddenCollections: Boolean\n  $numericTraits: [TraitRangeType!]\n  $paymentAssets: [PaymentAssetSymbol!]\n  $priceFilter: PriceFilterType\n  $query: String\n  $resultModel: SearchResultModel\n  $showContextMenu: Boolean = false\n  $shouldShowQuantity: Boolean = false\n  $sortAscending: Boolean\n  $sortBy: SearchSortBy\n  $stringTraits: [TraitInputType!]\n  $toggles: [SearchToggle!]\n  $creator: IdentityInputType\n  $assetOwner: IdentityInputType\n  $isPrivate: Boolean\n  $safelistRequestStatuses: [SafelistRequestStatus!]\n) {\n  query {\n    ...AssetSearch_data_2hBjZ1\n  }\n}\n\nfragment AssetCardContent_asset on AssetType {\n  relayId\n  name\n  ...AssetMedia_asset\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n  isDelisted\n}\n\nfragment AssetCardContent_assetBundle on AssetBundleType {\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          relayId\n          ...AssetMedia_asset\n          id\n        }\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_assetBundle on AssetBundleType {\n  name\n  assetCount\n  assetQuantities(first: 18) {\n    edges {\n      node {\n        asset {\n          collection {\n            name\n            relayId\n            isVerified\n            id\n          }\n          id\n        }\n        id\n      }\n    }\n  }\n  assetEventData {\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardFooter_asset_fdERL on AssetType {\n  ownedQuantity(identity: $identity) @include(if: $shouldShowQuantity)\n  name\n  tokenId\n  collection {\n    name\n    isVerified\n    id\n  }\n  hasUnlockableContent\n  isDelisted\n  isFrozen\n  assetContract {\n    address\n    chain\n    openseaVersion\n    id\n  }\n  assetEventData {\n    firstTransfer {\n      timestamp\n    }\n    lastSale {\n      unitPriceQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n  decimals\n  orderData {\n    bestBid {\n      orderType\n      paymentAssetQuantity {\n        ...AssetQuantity_data\n        id\n      }\n    }\n    bestAsk {\n      closedAt\n      orderType\n      dutchAuctionFinalPrice\n      openedAt\n      priceFnEndedAt\n      quantity\n      decimals\n      paymentAssetQuantity {\n        quantity\n        ...AssetQuantity_data\n        id\n      }\n    }\n  }\n}\n\nfragment AssetCardHeader_data_27d9G3 on AssetType {\n  relayId\n  favoritesCount\n  isDelisted\n  isFavorite\n  ...AssetContextMenu_data_3z4lq0 @include(if: $showContextMenu)\n}\n\nfragment AssetContextMenu_data_3z4lq0 on AssetType {\n  ...asset_edit_url\n  ...itemEvents_data\n  isDelisted\n  isEditable {\n    value\n    reason\n  }\n  isListable\n  ownership(identity: {}) {\n    isPrivate\n    quantity\n  }\n  creator {\n    address\n    id\n  }\n  collection {\n    isAuthorizedEditor\n    id\n  }\n}\n\nfragment AssetMedia_asset on AssetType {\n  animationUrl\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    id\n  }\n  isDelisted\n  displayImageUrl\n}\n\nfragment AssetQuantity_data on AssetQuantityType {\n  asset {\n    ...Price_data\n    id\n  }\n  quantity\n}\n\nfragment AssetSearchFilter_data_3KTzFc on Query {\n  ...CollectionFilter_data_2qccfC\n  collection(collection: $collection) {\n    numericTraits {\n      key\n      value {\n        max\n        min\n      }\n      ...NumericTraitFilter_data\n    }\n    stringTraits {\n      key\n      ...StringTraitFilter_data\n    }\n    id\n  }\n  ...PaymentFilter_data_2YoIWt\n}\n\nfragment AssetSearchList_data_3Aax2O on SearchResultType {\n  asset {\n    assetContract {\n      address\n      chain\n      id\n    }\n    collection {\n      isVerified\n      id\n    }\n    relayId\n    tokenId\n    ...AssetSelectionItem_data\n    ...asset_url\n    id\n  }\n  assetBundle {\n    relayId\n    id\n  }\n  ...Asset_data_3Aax2O\n}\n\nfragment AssetSearch_data_2hBjZ1 on Query {\n  ...CollectionHeadMetadata_data_2YoIWt\n  ...AssetSearchFilter_data_3KTzFc\n  ...SearchPills_data_2Kg4Sq\n  search(after: $cursor, chains: $chains, categories: $categories, collections: $collections, first: $count, identity: $identity, numericTraits: $numericTraits, paymentAssets: $paymentAssets, priceFilter: $priceFilter, querystring: $query, resultType: $resultModel, sortAscending: $sortAscending, sortBy: $sortBy, stringTraits: $stringTraits, toggles: $toggles, creator: $creator, isPrivate: $isPrivate, safelistRequestStatuses: $safelistRequestStatuses) {\n    edges {\n      node {\n        ...AssetSearchList_data_3Aax2O\n        __typename\n      }\n      cursor\n    }\n    totalCount\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment AssetSelectionItem_data on AssetType {\n  backgroundColor\n  collection {\n    displayData {\n      cardDisplayStyle\n    }\n    imageUrl\n    id\n  }\n  imageUrl\n  name\n  relayId\n}\n\nfragment Asset_data_3Aax2O on SearchResultType {\n  asset {\n    isDelisted\n    ...AssetCardHeader_data_27d9G3\n    ...AssetCardContent_asset\n    ...AssetCardFooter_asset_fdERL\n    ...AssetMedia_asset\n    ...asset_url\n    ...itemEvents_data\n    id\n  }\n  assetBundle {\n    ...bundle_url\n    ...AssetCardContent_assetBundle\n    ...AssetCardFooter_assetBundle\n    id\n  }\n}\n\nfragment CollectionFilter_data_2qccfC on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n      }\n    }\n  }\n  collections(assetOwner: $assetOwner, assetCreator: $creator, onlyPrivateAssets: $isPrivate, chains: $chains, first: 100, includeHidden: $includeHiddenCollections, parents: $categories, query: $collectionQuery, sortBy: $collectionSortBy) {\n    edges {\n      node {\n        assetCount\n        imageUrl\n        name\n        slug\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment CollectionHeadMetadata_data_2YoIWt on Query {\n  collection(collection: $collection) {\n    bannerImageUrl\n    description\n    imageUrl\n    name\n    id\n  }\n}\n\nfragment CollectionModalContent_data on CollectionType {\n  description\n  imageUrl\n  name\n  slug\n}\n\nfragment NumericTraitFilter_data on NumericTraitTypePair {\n  key\n  value {\n    max\n    min\n  }\n}\n\nfragment PaymentFilter_data_2YoIWt on Query {\n  paymentAssets(first: 10) {\n    edges {\n      node {\n        symbol\n        relayId\n        id\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n  PaymentFilter_collection: collection(collection: $collection) {\n    paymentAssets {\n      symbol\n      relayId\n      id\n    }\n    id\n  }\n}\n\nfragment Price_data on AssetType {\n  decimals\n  imageUrl\n  symbol\n  usdSpotPrice\n  assetContract {\n    blockExplorerLink\n    chain\n    id\n  }\n}\n\nfragment SearchPills_data_2Kg4Sq on Query {\n  selectedCollections: collections(first: 25, collections: $collections, includeHidden: true) {\n    edges {\n      node {\n        imageUrl\n        name\n        slug\n        ...CollectionModalContent_data\n        id\n      }\n    }\n  }\n}\n\nfragment StringTraitFilter_data on StringTraitType {\n  counts {\n    count\n    value\n  }\n  key\n}\n\nfragment asset_edit_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n  collection {\n    slug\n    id\n  }\n}\n\nfragment asset_url on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n\nfragment bundle_url on AssetBundleType {\n  slug\n}\n\nfragment itemEvents_data on AssetType {\n  assetContract {\n    address\n    chain\n    id\n  }\n  tokenId\n}\n",
#     "variables": {
#         "assetOwner": None,
#         "categories": None,
#         "chains": None,
#         "collection": None,
#         "collectionQuery": None,
#         "collectionSortBy": "SEVEN_DAY_VOLUME",
#         "collections": [],
#         "count": 32,
#         "creator": None,
#         "cursor": "YXJyYXljb25uZWN0aW9uOjMx",
#         "identity": None,
#         "includeHiddenCollections": False,
#         "isPrivate": None,
#         "numericTraits": None,
#         "paymentAssets": None,
#         "priceFilter": {"symbol": "USD", "min": 200},
#         "query": "",
#         "resultModel": None,
#         "safelistRequestStatuses": ["APPROVED", "VERIFIED"],
#         "shouldShowQuantity": False,
#         "showContextMenu": False,
#         "sortAscending": None,
#         "sortBy": None,
#         "stringTraits": None,
#         "toggles": None,
#     },
# }

# try get grafql payload

# collections: ["derpy-birbs"]

# assetContract {\n        address\n        id\n      }\n
# won't work
# defaultMintableAssetContract {\n          address\n          relayId\n          openseaVersion\n          id\n        }\n

# primary_asset_contracts
