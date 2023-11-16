from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement

def post_list(request):
        characters = Character.objects.all()
        equipements = Equipement.objects.all()
        context = {
        'characters': characters,
        'equipements': equipements,
        }

        return render(request, 'playground/post_list.html', context)
'''
def character_list(request):
    characters = Character.objects.filter()
    return render(request, 'playground/post_list.html', {'characters': characters})
'''

def character_detail(request, id_character):
    message = ''
    character = get_object_or_404(Character, id_character=id_character)
    lieu = character.lieu
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
    else:
        form = MoveForm()
    if form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        if nouveau_lieu.disponibilite == 'libre':
            if nouveau_lieu.id_equip == 'Lit':
                if character.etat=='fatigué':
                    character.etat='reveillé'
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas fatigué !"
                    return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
            if nouveau_lieu.id_equip == "Toilettes":
                if character.etat=='reveillé':
                    character.etat='affamé'
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas reveillé !"
                    return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
            if nouveau_lieu.id_equip == "Cuisine":
                if character.etat=='affamé':
                    character.etat='énergique'
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas affamé !"
                    return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
            if nouveau_lieu.id_equip == "Jardin":
                if character.etat=='énergique':
                    character.etat='sale'
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas énergique !"
                    return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
            if nouveau_lieu.id_equip == "Bain":
                if character.etat=='sale':
                    character.etat='fatigué'
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas sale !"
                    return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
        else:
            message = "Ce lieu est déjà occupé !"
            return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form, 'message': message},)
    
        form.save()
        character = get_object_or_404(Character, id_character=id_character)
        lieu = character.lieu
        return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
        return render(request,
                  'playground/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form})