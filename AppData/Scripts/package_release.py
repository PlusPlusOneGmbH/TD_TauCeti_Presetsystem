 

from subprocess import call

search_tag = "package_release_candidate"
release_candidates = parent.Project.findChildren( tags = [search_tag] )

# Lets release the proper dist to the actual repository for everyone to be able to fetch them directly without having to 
# select the correct branch.
for target in release_candidates:
    target.tags.remove(search_tag)
    op("PrivateInvestigator").Release( target )


call("uv version --bump patch")
import tomllib
with open("pyproject.toml", "rb") as projecttoml:
    projectdata = tomllib.load( projecttoml )
    version = projectdata["project"]["version"]

call("git add .")
call(f'git commit . -m "Bump to Version {version}"')

# Now lets prepare everything for a clean buildprocess.
# In the future all of this will run outside ;)

for target in release_candidates:
    for child in list( target.findChildren( tags = [op("PrivateInvestigator").par.Tag.eval()] ) ) + [target]:
        debug(f"Removing tag from {child}")
        child.tags.remove( op("PrivateInvestigator").par.Tag.eval() )
    
    prereleasescript = target.op("pre_release")
    if prereleasescript is not None: prereleasescript.run()
    op("PrivateInvestigator").Save( target )

call(f'git checkout -b v{version}')
call("git add .")
call(f'git commit . -m "TauCeti Release v{version}" ')




