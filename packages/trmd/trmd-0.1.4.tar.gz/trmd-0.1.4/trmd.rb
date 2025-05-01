class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/d8/04/5a7e196f0a536a3220f42c1b8749f253607f2513916c8748b31593d1a34e/trmd-0.1.3.tar.gz"
  sha256 "e6bd11a2a405a9d65399958836a982b3785bf0bb866dee94d59e904682851264"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
