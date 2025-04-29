import httpx
from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, List, Optional, Any

BASE_URL = "https://public.openrec.tv/external/api/v5"
mcp = FastMCP("OpenREC MCP Server")

@mcp.tool()
async def search_games(search_query: str) -> Dict[str, Any]:
    """
    ゲームを検索するツール

    Args:
        search_query: 検索キーワード

    Returns:
        検索結果のJSONデータ
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/search-games",
            params={"search_query": search_query}
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id": r.get("id"),
                "game_id": r.get("game_id"),
                "title": r.get("title"),
                "introduction": r.get("introduction"),
                "stats": r.get("stats")
            }
            for r in response.json()
        ]
        return response_json

@mcp.tool()
async def search_movies(
    search_query: str,
    sort: Optional[str] = None,
    include_deleted: Optional[bool] = None,
    channel_ids: Optional[str] = None,
    from_published_at: Optional[str] = None,
    to_published_at: Optional[str] = None,
    game_ids: Optional[str] = None,
    onair_status: Optional[int] = None,
    page: Optional[int] = None,
    include_live: Optional[bool] = None,
    include_upload: Optional[bool] = None
) -> Dict[str, Any]:
    """
    配信・動画を検索するツール

    Args:
        search_query: 検索キーワード
        sort: 並び順 (published_at: 登録が新しい順, -published_at: 登録が古い順, total_views: 視聴数順)
        include_deleted: 削除されたものを含めるか
        channel_ids: 検索対象の配信者のID
        from_published_at: ISO8601形式で指定した日時以降の動画一覧を取得
        to_published_at: ISO8601形式で指定した日時までの動画一覧を取得
        game_ids: ゲームIDを指定して検索をフィルタ
        onair_status: 0: 予約枠, 1: 配信中, 2: VOD
        page: ページ数
        include_live: 配信を含めるか
        include_upload: 投稿した動画を含めるか

    Returns:
        検索結果のJSONデータ
    """
    params = {"search_query": search_query}

    # オプションパラメータの追加
    if sort is not None:
        params["sort"] = sort
    if include_deleted is not None:
        params["include_deleted"] = include_deleted
    if channel_ids is not None:
        params["channel_ids"] = channel_ids
    if from_published_at is not None:
        params["from_published_at"] = from_published_at
    if to_published_at is not None:
        params["to_published_at"] = to_published_at
    if game_ids is not None:
        params["game_ids"] = game_ids
    if onair_status is not None:
        params["onair_status"] = onair_status
    if page is not None:
        params["page"] = page
    if include_live is not None:
        params["include_live"] = include_live
    if include_upload is not None:
        params["include_upload"] = include_upload

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/search-movies",
            params=params
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id" : r.get("id"),
                "movie_id" : str(r.get("movie_id")),
                "title" : r.get("title"),
                "introduction" : r.get("introduction"),
                "started_at" : r.get("started_at"),
                "ended_at" : r.get("ended_at"),
                "tags" : r.get("tags"),
                "channel" : {
                    "id" : r.get("channel",{}).get("id"),
                    "openrec_user_id" : r.get("channel",{}).get("openrec_user_id"),
                    "recxuser_id": r.get("channel",{}).get("recxuser_id"),
                    "nickname": r.get("channel",{}).get("nickname"),
                    "followers": r.get("channel",{}).get("followers"),
                    "movies": r.get("channel",{}).get("movies"),
                    "views": r.get("channel",{}).get("views"),
                },
                "game" : {
                    "id": r.get("game",{}).get("id"),
                    "game_id": r.get("game",{}).get("game_id"),
                    "title": r.get("game",{}).get("title"),
                    "introduction": r.get("introduction"),
                    "stats": r.get("stats")
                }
            }
            for r in response.json()
        ]

        return response_json

@mcp.tool()
async def get_movies(
    is_live: Optional[bool] = None,
    is_upload: Optional[bool] = None,
    onair_status: Optional[int] = None,
    channel_ids: Optional[str] = None,
    page: Optional[int] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    配信一覧を取得するツール

    Args:
        is_live: 取得するものを生配信に限定するか
        is_upload: 取得するものを動画に限定するか
        onair_status: 0は予約枠、1は配信中、2はVOD
        channel_ids: 特定のチャンネルのみに絞り込む
        page: ページ数（デフォルトは1）
        sort: 並び順(
            total_views | created_at | -created_at | schedule_at |
            onair_status | live_views | total_yells | -total_yells |
            popularity | published_at | -published_at
        )

    Returns:
        配信一覧のJSONデータ
    """
    params = {}

    if is_live is not None:
        params["is_live"] = is_live
    if is_upload is not None:
        params["is_upload"] = is_upload
    if onair_status is not None:
        params["onair_status"] = onair_status
    if channel_ids is not None:
        params["channel_ids"] = channel_ids
    if page is not None:
        params["page"] = page
    if sort is not None:
        params["sort"] = sort

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movies",
            params=params
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id" : r.get("id"),
                "movie_id": str(r.get("movie_id")),
                "title": r.get("title"),
                "introduction": r.get("introduction"),
                "started_at": r.get("started_at"),
                "ended_at": r.get("ended_at"),
                "popularity":r.get("popularity"),
                "tags": r.get("tags"),
                "channel" : {
                    "id" : r.get("channel",{}).get("id"),
                    "openrec_user_id" : r.get("channel",{}).get("openrec_user_id"),
                    "recxuser_id": r.get("channel",{}).get("recxuser_id"),
                    "nickname": r.get("channel",{}).get("nickname"),
                    "followers": r.get("channel",{}).get("followers"),
                    "movies": r.get("channel",{}).get("movies"),
                    "views": r.get("channel",{}).get("views"),
                },
                "game" : {
                    "id": r.get("game",{}).get("id"),
                    "game_id": r.get("game",{}).get("game_id"),
                    "title": r.get("game",{}).get("title"),
                    "introduction": r.get("introduction"),
                    "stats": r.get("stats")
                }
            }
            for r in response.json()
        ]
        return response_json


@mcp.tool()
async def get_movie_info(movie_id: str) -> Dict[str, Any]:
    """
    枠情報を取得するツール

    Args:
        movie_id: 動画ID（例: "n9ze3m2w184"）

    Returns:
        枠情報のJSONデータ
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movies/{movie_id}"
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id": response.json().get("id"),
                "movie_id": response.json().get("movie_id"),
                "title": response.json().get("title"),
                "intoduction": response.json().get("introduction"),
                "live_views": response.json().get("live_views"),
                "total_views": response.json().get("total_views"),
                "total_yells": response.json().get("total_yells"),
                "started_at": response.json().get("started_at"),
                "ended_at": response.json().get("ended_at"),
                "channel" : {
                    "id" : r.get("channel",{}).get("id"),
                    "openrec_user_id" : r.get("channel",{}).get("openrec_user_id"),
                    "recxuser_id": r.get("channel",{}).get("recxuser_id"),
                    "nickname": r.get("channel",{}).get("nickname"),
                    "followers": r.get("channel",{}).get("followers"),
                    "movies": r.get("channel",{}).get("movies"),
                    "views": r.get("channel",{}).get("views"),
                },
                "game" : {
                    "id": r.get("game",{}).get("id"),
                    "game_id": r.get("game",{}).get("game_id"),
                    "title": r.get("game",{}).get("title"),
                    "introduction": r.get("introduction"),
                    "stats": r.get("stats")
                },
                "popularity": r.get("popularity"),
            }
            for r in response.json()
        ]
        return response_json

@mcp.tool()
async def get_movie_chats(
    movie_id: str,
    from_created_at: Optional[str] = None,
    to_created_at: Optional[str] = None,
    is_including_system_message: Optional[bool] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    コメントの取得ツール

    Args:
        movie_id: 動画ID
        from_created_at: ISO8601形式で指定した日時以降のコメントを取得（例: 2023-03-20T12:48:47.265Z）
        to_created_at: ISO8601形式で指定した日時までのコメントを取得（from_created_atと同時に使用できない）
            - from_created_atとto_created_atのどちらかは、必ず指定する必要がある
        is_including_system_message: システムメッセージを含めるか
        limit: 取得するコメントの数（1-300）

    Returns:
        コメントのJSONデータ
    """
    params = {}

    if from_created_at is None and to_created_at is None:
        return {
            "error": "from_created_atとto_created_atのどちらかは、必ず指定する必要があります"
        }


    if from_created_at is not None:
        params["from_created_at"] = from_created_at
    if to_created_at is not None:
        params["to_created_at"] = to_created_at
    if is_including_system_message is not None:
        params["is_including_system_message"] = is_including_system_message
    if limit is not None:
        params["limit"] = limit
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/movies/{movie_id}/chats",
            params=params
        )
        
        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }
        
        response_json = [
            {
                "id": r.get("id"),
                "message": r.get("message"),
                "posted_at": r.get("created_at"),
                "user" : {
                    "id" : r.get("user",{}).get("id"),
                    "openrec_user_id" : r.get("user",{}).get("openrec_user_id"),
                    "nickname" : r.get("user",{}).get("nickname")
                }
            }
            for r in response.json()
        ]
        return response_json

@mcp.tool()
async def get_channel_ranks(
    period: Optional[str] = None,
    date: Optional[int] = None,
    tag: Optional[str] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    チャンネルランキングを取得するツール

    Args:
        period: ランキングの期間（hourly | daily | weekly | monthly）
        date: 月間ランキングの年月をYYYYMMの形式で指定
        tag: タグ（不明）
        page: ページ数（デフォルトは1）

    Returns:
        チャンネルランキングのJSONデータ
    """
    params = {}
    
    if period is not None:
        params["period"] = period
    if date is not None:
        params["date"] = date
    if tag is not None:
        params["tag"] = tag
    if page is not None:
        params["page"] = page
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/channel-ranks",
            params=params
        )
        
        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }
        
        response_json = [
            {
                "rank" : r.get("rank"),
                "total_views": r.get("total_views"),
                "playing_game" : {
                    "id": r.get("playing_game",{}).get("id"),
                    "game_id": r.get("playing_game",{}).get("game_id"),
                    "title": r.get("playing_game",{}).get("title"),
                    "introduction": r.get("playing_game",{}).get("introduction"),
                    "stats": r.get("playing_game",{}).get("stats")
                },
                "channel" : {
                    "id" : r.get("channel",{}).get("id"),
                    "openrec_user_id" : r.get("channel",{}).get("openrec_user_id"),
                    "recxuser_id": r.get("channel",{}).get("recxuser_id"),
                    "nickname": r.get("channel",{}).get("nickname"),
                    "followers": r.get("channel",{}).get("followers"),
                    "movies": r.get("channel",{}).get("movies"),
                    "views": r.get("channel",{}).get("views"),
                },
            }
            for r in response.json()
        ]
        return response_json

@mcp.tool()
async def get_popular_channels(page: Optional[int] = None) -> Dict[str, Any]:
    """
    人気チャンネルを取得するツール

    Args:
        page: ページ数（デフォルトは1）

    Returns:
        人気チャンネルのJSONデータ
    """
    params = {}

    if page is not None:
        params["page"] = page

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/popular-channels",
            params=params
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id" : r.get("id"),
                "openrec_user_id" : r.get("openrec_user_id"),
                "recxuser_id": r.get("recxuser_id"),
                "nickname": r.get("nickname"),
                "introduction": r.get("introduction"),
                "followers": r.get("followers"),
                "movies": r.get("movies"),
                "views": r.get("views"),
            }
            for r in response.json()
        ]
        return response_json

@mcp.tool()
async def get_popular_movies(
    popular_type: Optional[str] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    人気動画一覧を取得するツール

    Args:
        popular_type: 取得するタイプ（archive | upload | upload_archive）
        page: ページ数（デフォルトは1）

    Returns:
        人気動画一覧のJSONデータ
    """
    params = {}

    if popular_type is not None:
        params["popular_type"] = popular_type
    if page is not None:
        params["page"] = page

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/popular-movies",
            params=params
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id" : r.get("id"),
                "movie_id": str(r.get("movie_id")),
                "title": r.get("title"),
                "introduction": r.get("introduction"),
                "started_at": r.get("started_at"),
                "ended_at": r.get("ended_at"),
                "tags": r.get("tags"),
                "channel" : {
                    "id" : r.get("channel",{}).get("id"),
                    "openrec_user_id" : r.get("channel",{}).get("openrec_user_id"),
                    "recxuser_id": r.get("channel",{}).get("recxuser_id"),
                    "nickname": r.get("channel",{}).get("nickname"),
                    "followers": r.get("channel",{}).get("followers"),
                    "movies": r.get("channel",{}).get("movies"),
                    "views": r.get("channel",{}).get("views"),
                },
                "game" : {
                    "id": r.get("game",{}).get("id"),
                    "game_id": r.get("game",{}).get("game_id"),
                    "title": r.get("game",{}).get("title"),
                    "introduction": r.get("introduction"),
                    "stats": r.get("stats")
                }
            }
            for r in response.json()
        ]
        return response_json

# @mcp.tool()
# async def get_yell_logs(
#     movie_id: str,
#     page: Optional[int] = None
# ) -> Dict[str, Any]:
#     """
#     時系列順エールを取得するツール

#     Args:
#         movie_id: 動画ID
#         page: ページ数（デフォルトは1）

#     Returns:
#         時系列順エールのJSONデータ
#     """
#     params = {"movie_id": movie_id}
#     if page is not None:
#         params["page"] = page
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"{BASE_URL}/yell-logs",
#             params=params
#         )
#         if response.status_code != 200:
#             return {
#                 "error": f"APIリクエストエラー: {response.status_code}",
#                 "message": response.text
#             }
#         return response.json()

@mcp.tool()
async def get_popular_games(page: Optional[int] = None) -> Dict[str, Any]:
    """
    人気ゲーム一覧を取得するツール

    Args:
        page: ページ数（デフォルトは1）

    Returns:
        人気ゲーム一覧のJSONデータ
    """
    params = {}

    if page is not None:
        params["page"] = page

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/popular-games",
            params=params
        )

        if response.status_code != 200:
            return {
                "error": f"APIリクエストエラー: {response.status_code}",
                "message": response.text
            }

        response_json = [
            {
                "id": r.get("id"),
                "game_id": r.get("game_id"),
                "title": r.get("title"),
                "introduction": r.get("introduction"),
                "stats": r.get("stats")
            }
            for r in response.json()
        ]
        return response_json

def main():
    """Main entry point for the OpenREC API server."""
    print("Starting OpenREC API server...")
    mcp.run()

if __name__ == "__main__":
    main()