#coding:utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post ,Category ,Tag
import markdown
from comments.forms import CommentForm

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView, DetailView




# Create your views here.

def index(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,2)
    page=request.GET.get('page')

    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/index.html',
        {'title':'my blog index',
         'welcome':'welcome to my blog index',
         'post_list':post_list
         }
        #context={'title':'','welcome':''}
        )
#分页等价类视图

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        paginator=context.get('paginator')
        page=context.get('page_obj')
        is_paginated=context.get('is_paginated')

        pagination_data=self.pageination_data(paginator,page,is_paginated)

        context.update(pagination_data)

        return context

    def pageination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}

        left=[]
        right=[]

        left_has_more=False
        right_has_more=False

        first=False
        last=False

        page_number=page.number
        total_pages=paginator.num_pages
        page_range=paginator.page_range

        #第一夜
        if page_number==1:
            right=page_range[page_number:page_number+2]

            if right[-1]<total_pages - 1:
                right_has_more=True

            if right[-1]<total_pages:
                last=True
        #最后一夜
        elif page_number == total_pages:

            left=page_range[(page_number - 3) if (page_number - 3) >0 else 0 :page_number -1]

            if left[0]>2:
                left_has_more=True

            if left[0]>1:
                first = True

        else:
            right = page_range[page_number:page_number + 2]
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if right[-1]<total_pages - 1:
                right_has_more=True

            if right[-1]<total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        context={
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }

        return context


def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.increase_views()
    md=markdown.Markdown(post.content,extensions=['markdown.extensions.extra',
                                                  'markdown.extensions.codehilite',  #代码高亮拓展
                                                  TocExtension(slugify=slugify),  #美化描点URL
                                                  #'markdown.extensions.toc',  #自动生成目录的拓展
                                                  ])
    post.content=md.convert(post.content)
    form=CommentForm()
    comment_list=post.comment_set.all()

    context={
        'post':post,
        'toc':md.toc,
        'form':form,
        'comment_list':comment_list
    }

    return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    
    def get(self,request,*args,**kwargs):
        response=super(PostDetailView, self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post=super(PostDetailView, self).get_object(queryset=None)
        post.content=markdown.markdown(post.content,extensions=['markdown.extensions.extra',
                                                                'markdown.extensions.codehilite',  #代码高亮拓展
                                                                 TocExtension(slugify=slugify),  #美化描点URL
                                                                 #'markdown.extensions.toc',  #自动生成目录的拓展
                                                  ])
        return post
    def get_context_data(self, **kwargs):
        context=super(PostDetailView, self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context

        





def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by('-created_time')
    return render(request,'blog/index.html',{'post_list':post_list})

class ArchivesView(IndexView):

    def get_queryset(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,
                                  created_time__month=month)


def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',{'post_list':post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

def search(request):
    q=request.GET.get('q')
    error_msg=''
    if not q:
        error_msg='请输入关键字'
        return render(request,'blog/index.html',{'error_msg':error_msg})

    post_list=Post.objects.filter(title__icontains=q)
    return render(request,'blog/index.html',{'error_msg':error_msg,'post_list':post_list})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    content_object_name='post_list'

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

