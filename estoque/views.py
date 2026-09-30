from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Material
from .forms import MaterialForm


def dashboard(request):
    materiais = Material.objects.all()

    faltantes = [m for m in materiais if m.estoque_baixo]
    vencidos = [m for m in materiais if m.vencido]
    proximos_vencimento = [m for m in materiais if m.proximo_vencimento]

    context = {
        'total_materiais': materiais.count(),
        'faltantes': faltantes,
        'vencidos': vencidos,
        'proximos_vencimento': proximos_vencimento,
        'qtd_faltantes': len(faltantes),
        'qtd_vencidos': len(vencidos),
        'qtd_proximos_vencimento': len(proximos_vencimento),
    }

    return render(request, 'estoque/dashboard.html', context)


def cadastrar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MaterialForm()

    return render(request, 'estoque/cadastrar_material.html', {'form': form})


def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        validade_atual = material.data_validade

        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            material = form.save(commit=False)
            material.data_validade = validade_atual
            material.save()

            return redirect('dashboard')

    else:
        form = MaterialForm(instance=material)

    return render(
        request,
        'estoque/editar_material.html',
        {'form': form, 'material': material}
    )

def excluir_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        material.delete()
        return redirect('dashboard')

    return render(request, 'estoque/excluir_material.html', {'material': material})


def listar_materiais(request):
    materiais = Material.objects.all()

    busca = request.GET.get('busca', '')
    categoria = request.GET.get('categoria', '')

    if busca:
        materiais = materiais.filter(nome__icontains=busca)

    if categoria:
        materiais = materiais.filter(categoria=categoria)

    context = {
        'materiais': materiais,
        'busca': busca,
        'categoria': categoria,
        'categorias': Material.CATEGORIA_CHOICES,
    }

    return render(request, 'estoque/listar_materiais.html', context)


def gerar_relatorio_pdf(request):
    materiais = Material.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setTitle("Relatório de Estoque")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "Relatório de Estoque")

    y = 760

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Material")
    pdf.drawString(200, y, "Categoria")
    pdf.drawString(300, y, "Atual")
    pdf.drawString(350, y, "Mínimo")
    pdf.drawString(410, y, "Validade")

    y -= 20
    pdf.setFont("Helvetica", 9)

    for material in materiais:
        pdf.drawString(50, y, material.nome[:25])
        pdf.drawString(200, y, material.get_categoria_display())
        pdf.drawString(300, y, str(material.quantidade_atual))
        pdf.drawString(350, y, str(material.quantidade_minima))
        pdf.drawString(
            410,
            y,
            str(material.data_validade or "Não informada")
        )

        y -= 18

        if y < 50:
            pdf.showPage()
            y = 800
            pdf.setFont("Helvetica", 9)

    pdf.save()

    return response

def entrada_validade(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        material.data_validade = request.POST.get('data_validade')
        material.save()
        return redirect('editar_material', pk=material.id)

    return render(
        request,
        'estoque/entrada_validade.html',
        {'material': material}
    )