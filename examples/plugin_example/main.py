import magic
import os

nature = magic.new_domain(name="nature", global=True, directory=os.join(__file__, "plugins"))

nature_domain = nature.__domain__

bird_versions = nature_domain.get_versions_of("animal.bird") # set(["0.5.0", "0.6.0"])
nature_domain.prefer_version_of("animal.bird", nature_domain.sort_versions(bird_version)[-1]) # prefer oldest version

import logic

logic.do_some_stuff()
