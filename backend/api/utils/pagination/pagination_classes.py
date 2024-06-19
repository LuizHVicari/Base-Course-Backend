from rest_framework.pagination import PageNumberPagination

# by default, all page size query params will be set as 'page_size'

QUERY_PARAM = 'page_size'

class StandardPagination(PageNumberPagination):
  """
  Pagination class with stardard 20 and max 100
  """
  page_size = 20
  page_size_query_param = QUERY_PARAM
  max_page_size = 100