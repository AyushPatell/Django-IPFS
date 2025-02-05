import ipfshttpclient
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileForm
from .models import File

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
            res = client.add(file)
            File.objects.create(name=file.name, ipfs_hash=res['Hash'])
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'upload.html', {'form': form})

def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    file_data = client.cat(file.ipfs_hash)
    response = HttpResponse(file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})