import copy
from django.utils.safestring import mark_safe
from django.http.request import QueryDict


class Pagination(object):

    def __init__(self, request, queryset, page_size, page_param="page", plus=3):

        queryset_dict = copy.deepcopy(request.GET)
        queryset_dict._mutable = True
        self.queryset_dict = queryset_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        if total_count:
            total_page_count, div = divmod(total_count, page_size)
            if div:
                total_page_count += 1
        else:
            total_page_count = 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []

        # 上一页和最小极值处理
        if self.page > 1:
            self.queryset_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}" aria-label="Previous">«</a></li>'.format(self.queryset_dict.urlencode())
        else:
            self.queryset_dict.setlist(self.page_param, [1])
            prev = '<li class = "disabled"><a href="?{}" aria-label="Previous">«</a></li>'.format(
                self.queryset_dict.urlencode())
        page_str_list.append(prev)

        # 首页处理
        if self.page == self.plus + 2 and self.total_page_count != 5:
            self.queryset_dict.setlist(self.page_param, [1])
            page_str_list.append('<li><a href="?{}">1</a></li>'.format(self.queryset_dict.urlencode()))
        if self.page > self.plus + 2:
            self.queryset_dict.setlist(self.page_param, [1])
            page_str_list.append('<li><a href="?{}">1..</a></li>'.format(self.queryset_dict.urlencode()))

        # 当前页及前后plus页
        for i in range(start_page, end_page + 1):
            self.queryset_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.queryset_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.queryset_dict.urlencode(), i)
            page_str_list.append(ele)

        # 尾页处理
        if self.page == self.total_page_count - self.plus - 1 and self.total_page_count != 5:
            self.queryset_dict.setlist(self.page_param, [self.total_page_count])
            page_str_list.append(
                '<li><a href="?{}">{}</a></li>'.format(self.queryset_dict.urlencode(), self.total_page_count))
        if self.page < self.total_page_count - self.plus - 1:
            self.queryset_dict.setlist(self.page_param, [self.total_page_count])
            page_str_list.append(
                '<li><a href="?{}">..{}</a></li>'.format(self.queryset_dict.urlencode(), self.total_page_count))

        # 下一页和最大极值处理
        if self.page < self.total_page_count:
            self.queryset_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}" aria-label="Next">»</a></li>'.format(self.queryset_dict.urlencode())
        else:
            self.queryset_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li class = "disabled"><a href="?{}" aria-label="Next">»</a></li>'.format(
                self.queryset_dict.urlencode())
        page_str_list.append(next)

        page_string = mark_safe("".join(page_str_list))
        return page_string
