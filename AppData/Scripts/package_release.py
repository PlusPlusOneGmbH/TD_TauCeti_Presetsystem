 
search_tag = "package_release_candidate"

for target in parent.Project.findChildren( tags = [search_tag]):
    
    target.tags.remove(search_tag)
    target.tags.remove( op("PrivateInvestigator").par.Tag.eval() )
    
    prereleasescript = target.op("pre_release")
    if prereleasescript is not None: prereleasescript.run()
    op("PrivateInvestigator").Save( target )
    op("PrivateInvestigator").Release( target )


from subprocess import call
# call("uv version --bump minor")

import tomllib
with open("pyproject.toml", "rb") as projecttoml:
    projectdata = tomllib.load( projecttoml )
    version = projectdata["project"]["version"]

call(f'git checkout -b v{version}')
call("git add .")
call(f'git commit . -m "TauCeti Release v{version}" ')
# call(f'git tag -a v{version} -m "TauCeti Release v{version}"')




