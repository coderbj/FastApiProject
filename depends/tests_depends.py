from fastapi import Query


async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60)
):
    return {'skip': skip, 'limit': limit}
