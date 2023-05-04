import pickle
from sys import argv

# def generate_plot(folder: str) -> None:
# generate_plot('')

with open(f'./matplotimages/{argv[2]}', 'rb') as handle:
    print('opa')
    cidade = pickle.load(handle)
    fig = cidade.plot()
    print('gerando imagem')
    # Hide X and Y axes label marks
    fig.xaxis.set_tick_params(labelbottom=False)
    fig.yaxis.set_tick_params(labelleft=False)
    fig.set_xticks([])
    fig.set_yticks([])

    fig.set_facecolor('#FAFAFA')
    fig.get_figure().savefig(f'./matplotimages/{argv[2]}.png', bbox_inches='tight')

# Convém deletar arquivo .pickle depois de usar
