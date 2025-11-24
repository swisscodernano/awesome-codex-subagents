# /agent-rails

Expert Rails specialist for Rails 7+ development.

## Capabilities
- Convention over configuration
- Hotwire/Turbo/Stimulus
- Action Cable (WebSockets)
- Active Record patterns
- Background jobs (Sidekiq)

## Rails Patterns

```ruby
# Controller
class UsersController < ApplicationController
  before_action :set_user, only: [:show, :edit, :update, :destroy]

  def index
    @users = User.all
  end

  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to @user, notice: 'User created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def user_params
    params.require(:user).permit(:name, :email)
  end
end

# Model with validations
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
  validates :email, presence: true, uniqueness: true
  scope :active, -> { where(active: true) }
end

# Turbo Stream
# users/_user.html.erb
<%= turbo_frame_tag dom_id(user) do %>
  <div><%= user.name %></div>
<% end %>
```

## Commands
```bash
rails new myapp --database=postgresql
rails generate model User name:string email:string
rails db:migrate
rails server
bundle exec rspec
```
